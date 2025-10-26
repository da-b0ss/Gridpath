import sys
from src.data_loader import load_challenge_data
from src.routing import solve_missions
from src.visualize import plot_solution
from src import config

def run_pipeline():
    """
    Main pipeline for the NextEra Drone Challenge.
    """
    try:
        # 1. Load Data
        data = load_challenge_data()
        
        # --- Define the Drone Fleet ---
        # This is where your frontend/API will send its configuration.
        standard_cap = config.STANDARD_BATTERY_CAPACITY

        # --- OPTION 1: A standard fleet with a 5% safety margin ---
        num_drones = 30
        safety_margin = 0.95
        default_capacity = int(standard_cap) #(standard_cap * safety_margin)
        fleet_capacities = [default_capacity] * num_drones


        #Test hetergenous fleet
        #fleet_capacities = [default_capacity] * num_drones
        #fleet_capacities[0] = int(standard_cap * 0.80)  # Drone 1 (80% capacity "Used")
        #fleet_capacities[1] = int(standard_cap * 0.60)   # Drone 2(60% capacity "Lemon")
        #fleet_capacities[2] = int(standard_cap * 0.60)   # Drone 3(60% capacity "Lemon")
        #fleet_capacities[3] = int(standard_cap * 0.40)   # Drone 4(40% capacity "Damaged by intern")
        #fleet_capacities[4] = int(standard_cap * 0.40)   # Drone 4(40% capacity "Damaged by intern")
        #fleet_capacities[5] = int(standard_cap * 0.10)   # Drone 4(40% capacity "Damaged by intern")

        # --- OPTION 2: A fully custom fleet with unique drones ---
        # 4 drones: 2 new, 1 used (80%), 1 lemon (60%)
        # This list can have any number of drones with any unique capacities.
        # fleet_capacities = [
        #     int(standard_cap * 0.95),  # Drone 1 (95% capacity)
        #     int(standard_cap * 0.95),  # Drone 2 (95% capacity)
        #     int(standard_cap * 0.80),  # Drone 3 (80% capacity "Used")
        #     int(standard_cap * 0.60)   # Drone 4 (60% capacity "Lemon")
        # ]
        # --- End of Fleet Definition ---

        print(f"Solving for a fleet of {len(fleet_capacities)} drones.")
        print(f"Capacities: {fleet_capacities}")

        # 2. Solve Routing
        # 'missions' is a list of lists, where each sublist
        # is the sequence of *stops* (waypoint indices)
        print("Calling solve_missions with vehicle_capacities:", fleet_capacities)
        missions = solve_missions(data, vehicle_capacities=fleet_capacities)
        
        if not missions:
            print("Could not find a valid solution.")
            return

        # 3. Visualize
        # The plot function will use the predecessors matrix
        # to reconstruct the full paths between stops.
        plot_solution(missions, data)

    except FileNotFoundError as e:
        print(f"Error: Data file not found. {e}", file=sys.stderr)
        print("Please ensure all .npy and .wkt files are in the 'data/' directory.", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    run_pipeline()