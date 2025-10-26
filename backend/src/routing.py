import numpy as np
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from src import config
import random

SEARCH_TIME_LIMIT_SECONDS = 60

def create_solver_data_model(data: dict, vehicle_capacities: list[int]) -> dict:
    """Prepares data for the OR-Tools solver."""
    
    # Ensure all indices are within bounds
    valid_waypoints = [wp for wp in data['required_waypoints'] if wp < len(data['distance_matrix'])]
    locations = [config.DEPOT_INDEX] + valid_waypoints
    
    # Map from solver's internal index (0, 1, 2...)
    # back to the original waypoint index (0, 1501, 1502...)
    solver_to_waypoint = {i: loc for i, loc in enumerate(locations)}
    
    # Create the smaller distance matrix just for these locations
    num_locations = len(locations)
    solver_dist_matrix = np.zeros((num_locations, num_locations), dtype=np.int64)
    
    for from_i in range(num_locations):
        for to_j in range(num_locations):
            from_waypoint = solver_to_waypoint[from_i]
            to_waypoint = solver_to_waypoint[to_j]
            solver_dist_matrix[from_i, to_j] = data['distance_matrix'][from_waypoint, to_waypoint]
            
    return {
        'solver_dist_matrix': solver_dist_matrix,
        'solver_to_waypoint': solver_to_waypoint,
        'num_vehicles': len(vehicle_capacities),
        'vehicle_capacities': vehicle_capacities,
        'depot': 0 # The depot is ALWAYS index 0 for the solver
    }

def set_metaheuristic(search_parameters, name: str):
    name = name.upper()
    if name == "GLS":
        search_parameters.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    elif name == "SA":
        search_parameters.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.SIMULATED_ANNEALING
    elif name == "TABU":
        search_parameters.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH
    else:
        search_parameters.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.AUTOMATIC


def build_seed_routes_from_permutation(perm, num_vehicles, max_route_len):
    """
    perm: list of solver node ids excluding depot (0).
    Splits perm into <= num_vehicles routes (naive length-based split).
    You can replace the splitter with battery-aware splitting if desired.
    """
    routes = [[] for _ in range(num_vehicles)]
    v, count = 0, 0
    for node in perm:
        routes[v].append(node)
        count += 1
        if count >= max_route_len and v < num_vehicles - 1:
            v += 1
            count = 0
    return routes

def make_eval_distance(model):
    """
    Returns eval_distance(routes): penalty-based score for GA.
    """
    dist = model['solver_dist_matrix']
    depot = 0
    # Per-vehicle hard limit (battery). Here we use one shared limit from config for all.
    # If you have per-vehicle limits, pass a list instead.
    limit = getattr(config, "STANDARD_BATTERY_CAPACITY", 10**9)

    def route_cost(r):
        used = 0
        prev = depot
        for n in r:
            used += dist[prev, n]
            prev = n
        used += dist[prev, depot]
        return used

    def eval_distance(routes):
        total = 0
        for r in routes:
            c = route_cost(r)
            total += c
            if c > limit:
                # soft penalty if a route violates the limit
                total += 1_000_000 + 1_000 * (c - limit)
        return total
    return eval_distance

def ga_build_seed(num_nodes, num_vehicles, eval_distance,
                  generations=120, pop_size=80, max_route_len=50, mutation_p=0.25):
    """
    Minimal GA that evolves permutations of customers (1..num_nodes-1).
    Returns best routes (list of solver-node lists, excluding depot).
    """
    customers = list(range(1, num_nodes))

    def make_ind():
        ind = customers[:]
        random.shuffle(ind)
        return ind

    def score_perm(perm):
        routes = build_seed_routes_from_permutation(perm, num_vehicles, max_route_len)
        return routes, eval_distance(routes)

    def mutate(perm):
        if random.random() < mutation_p:
            i, j = sorted(random.sample(range(len(perm)), 2))
            perm[i:j] = reversed(perm[i:j])
        return perm

    def crossover(p1, p2):
        # simple order-crossover (OX)
        a, b = sorted(random.sample(range(len(p1)), 2))
        hole = set(p1[a:b])
        child = p1[:a] + [x for x in p2 if x not in hole] + p1[a:b]
        return child

    # init population
    scored = [(make_ind(), None) for _ in range(pop_size)]
    scored = [(perm, score_perm(perm)) for (perm, _) in scored]

    for _ in range(generations):
        # tournament selection
        parents = [min(random.sample(scored, 3), key=lambda x: x[1][1])[0] for _ in range(pop_size)]
        children = []
        for i in range(0, pop_size, 2):
            p1 = parents[i]
            p2 = parents[i+1 if i+1 < pop_size else 0]
            c = crossover(p1, p2)
            c = mutate(c)
            children.append(c)
        scored = [(perm, score_perm(perm)) for perm in children]

    best_perm, (best_routes, best_score) = min(scored, key=lambda x: x[1][1])
    return best_routes

def run_alns_seed(routing, manager, time_seconds=SEARCH_TIME_LIMIT_SECONDS, first_sol="PATH_MOST_CONSTRAINED_ARC", ls="GLS"):

    params = pywrapcp.DefaultRoutingSearchParameters()
    # solid constructive start so LNS has structure
    params.first_solution_strategy = getattr(routing_enums_pb2.FirstSolutionStrategy, first_sol)
    # adaptive operator selection = the "A" in ALNS
    params.use_multi_armed_bandit_concatenate_operators = True
    set_metaheuristic(params, ls)  # e.g., GLS / SA / TABU
    params.log_search = True
    params.time_limit.seconds = time_seconds
    seed_solution = routing.SolveWithParameters(params)
    return seed_solution

def improve_from_routes(routing, routes, time_seconds=SEARCH_TIME_LIMIT_SECONDS, ls="GLS"):
    params = pywrapcp.DefaultRoutingSearchParameters()
    set_metaheuristic(params, ls)
    params.use_multi_armed_bandit_concatenate_operators = True
    params.log_search = True
    params.time_limit.seconds = time_seconds

    initial = routing.ReadAssignmentFromRoutes(routes, True)
    if initial:
        sol = routing.SolveFromAssignmentWithParameters(initial, params)
        if sol:
            return sol
    # Fallback: just try normal solve with these params
    return routing.SolveWithParameters(params)

def validate_input_data(data: dict, vehicle_capacities: list[int]) -> bool:
    """Validates the input data for the solver."""
    if not isinstance(vehicle_capacities, list) or not all(isinstance(cap, int) and cap > 0 for cap in vehicle_capacities):
        print("Error: vehicle_capacities must be a list of positive integers.")
        return False

    if 'distance_matrix' not in data or not isinstance(data['distance_matrix'], np.ndarray):
        print("Error: distance_matrix must be a NumPy array.")
        return False

    if 'required_waypoints' not in data or not isinstance(data['required_waypoints'], list):
        print("Error: required_waypoints must be a list.")
        return False

    print("Input data validation passed.")
    return True

def solve_missions(data: dict, vehicle_capacities: list[int], strategy_name: str = "DEFAULT") -> list[list[int]]:
    print("solve_missions function called with vehicle_capacities:", vehicle_capacities)

    # Validate input data
    if not validate_input_data(data, vehicle_capacities):
        return []

    """
    Solves the CVRP via a 3-stage pipeline:
      A) ALNS seed  -> OR-Tools adaptive LNS
      B) GA seed    -> genetic global pathing (build routes)
      C) Memetic    -> OR-Tools local-search refinement from GA seed
    Returns missions as lists of *original waypoint indices*.
    """
    model = create_solver_data_model(data, vehicle_capacities=vehicle_capacities)
    manager = pywrapcp.RoutingIndexManager(
        len(model['solver_dist_matrix']),
        model['num_vehicles'],
        model['depot']
    )
    routing = pywrapcp.RoutingModel(manager)

    # 1) Distance callback (unchanged)
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return model['solver_dist_matrix'][from_node, to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # 2) Battery/Distance dimension (unchanged)
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        config.STANDARD_BATTERY_CAPACITY,
        True,  # start at zero
        'Distance'
    )
    distance_dimension = routing.GetDimensionOrDie('Distance')  # noqa: F841

    # === PIPELINE WALL-CLOCK SPLIT (tune as you like) ===
    t_alns = 20   # seconds for Stage A (ALNS)
    t_ga   = 25   # seconds "budget" for GA outer loop (approx; GA is CPU-bound)
    t_ma   = 45   # seconds for Stage C (memetic refinement)

       # 3. Set search parameters and solve
    # === Stage A: ALNS seed ===
    params_seed = pywrapcp.DefaultRoutingSearchParameters()
    params_seed.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_MOST_CONSTRAINED_ARC
    )
    # Adaptive operator selection (the “A” in ALNS)
    params_seed.use_multi_armed_bandit_concatenate_operators = True
    # A good LS for ALNS seeding (try SA/TABU if your instance prefers it)
    params_seed.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    params_seed.solution_limit = 100
    params_seed.log_search = True
    # Give the seed a smaller slice of time
    params_seed.time_limit.seconds = 20

    print("Stage A: ALNS seeding…")
    seed_solution = routing.SolveWithParameters(params_seed)

    # === Stage B: Memetic refinement (improve from seed) ===
    solution = None
    if seed_solution:
        params_refine = pywrapcp.DefaultRoutingSearchParameters()
        # Keep adaptive LNS operators, but push a different metaheuristic to diversify
        params_refine.use_multi_armed_bandit_concatenate_operators = True
        params_refine.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.TABU_SEARCH
        )
        params_refine.solution_limit = 100
        params_refine.log_search = True
        # Spend the rest of the budget polishing
        params_refine.time_limit.seconds = 60

        print("Stage B: Memetic refinement (improve from ALNS seed)…")
        solution = routing.SolveFromAssignmentWithParameters(seed_solution, params_refine)

    # Fallback: single-stage AUTOMATIC if seed fails (rare)
    if not solution:
        params_fallback = pywrapcp.DefaultRoutingSearchParameters()
        params_fallback.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_MOST_CONSTRAINED_ARC
        )
        params_fallback.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.AUTOMATIC
        )
        params_fallback.use_multi_armed_bandit_concatenate_operators = True
        params_fallback.solution_limit = 100
        params_fallback.log_search = True
        params_fallback.time_limit.seconds = 90
        print("Fallback: single-stage AUTOMATIC…")
        solution = routing.SolveWithParameters(params_fallback)


    if not solution:
        # Last-resort single-stage solve with your original defaults
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        set_metaheuristic(search_parameters, "AUTOMATIC")
        search_parameters.use_multi_armed_bandit_concatenate_operators = True
        search_parameters.solution_limit = 100
        search_parameters.log_search = True
        search_parameters.time_limit.seconds = 90
        solution = routing.SolveWithParameters(search_parameters)

    if not solution:
        print("No solution found!")
        return []

    # 4) Parse the solution (unchanged)
    missions = []
    total_distance = 0
    for vehicle_id in range(model['num_vehicles']):
        index = routing.Start(vehicle_id)
        route = []
        route_distance = 0

        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route.append(model['solver_to_waypoint'][node_index])

            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
        # Add the depot at the end
        node_index = manager.IndexToNode(index)
        route.append(model['solver_to_waypoint'][node_index])

        if len(route) > 2: # It's not an empty route
            missions.append(route)
            total_distance += route_distance
            print(f"Vehicle {vehicle_id}: distance={route_distance}ft, stops={len(route)-2}")

    print(f"\nSolution found: {len(missions)} missions.")
    print(f"Total distance for all missions: {total_distance} feet.")
    return missions
