import sys
import os
import json
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
        # Check if fleet configuration file exists (created by API)
        fleet_config_path = os.path.join(os.path.dirname(__file__), 'data', 'fleet_config.json')

        if os.path.exists(fleet_config_path):
            # Load fleet configuration from file
            with open(fleet_config_path, 'r') as f:
                fleet_config = json.load(f)
                fleet_capacities = fleet_config.get('fleet_capacities', [])

            print(f"Loaded fleet configuration from file: {len(fleet_capacities)} drones")
        else:
            # Use default configuration
            standard_cap = config.STANDARD_BATTERY_CAPACITY
            num_drones = 30
            default_capacity = int(standard_cap)
            fleet_capacities = [default_capacity] * num_drones

            print(f"Using default fleet configuration: {num_drones} drones")

        # --- Define the Solver Strategy ---
        # This string must match one of the options in routing.py

        # A good, fast, high-quality default.
        solver_strategy = "FAST_QUALITY" 

        # Your original strategy
        # solver_strategy = "DEFAULT" 

        # A strategy for getting the absolute best score, given more time
        # solver_strategy = "BEST_QUALITY" 
        #
        # --- End of Strategy Definition ---

        print(f"Solving for a fleet of {len(fleet_capacities)} drones.")
        print(f"Capacities: {fleet_capacities}")

        # 2. Solve Routing
        # 'missions' is a list of lists, where each sublist
        # is the sequence of *stops* (waypoint indices)
        print("Calling solve_missions with vehicle_capacities:", fleet_capacities)
        missions = solve_missions(data, vehicle_capacities=fleet_capacities, strategy_name=solver_strategy)
        
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