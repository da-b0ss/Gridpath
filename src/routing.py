import numpy as np
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from src import config

def create_solver_data_model(data: dict) -> dict:
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
        'num_vehicles': config.NUM_VEHICLES,
        'depot': 0 # The depot is ALWAYS index 0 for the solver
    }

def solve_missions(data: dict) -> list[list[int]]:
    """
    Solves the CVRP and returns a list of missions.
    Each mission is a list of *original waypoint indices*.
    """
    model = create_solver_data_model(data)
    manager = pywrapcp.RoutingIndexManager(
        len(model['solver_dist_matrix']),
        model['num_vehicles'],
        model['depot']
    )
    routing = pywrapcp.RoutingModel(manager)

    # 1. Create the distance callback
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return model['solver_dist_matrix'][from_node, to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # 2. Add the battery distance constraint
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        config.MAX_MISSION_DISTANCE_FEET,
        True,  # Start cumulative distance at zero
        'Distance'
    )
    distance_dimension = routing.GetDimensionOrDie('Distance')

    # 3. Set search parameters and solve
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_parameters.time_limit.seconds = 30 # Add a 30s time limit

    print("Solving... (This may take up to 30 seconds)")
    solution = routing.SolveWithParameters(search_parameters)
    
    if not solution:
        print("No solution found!")
        return []

    # 4. Parse the solution
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