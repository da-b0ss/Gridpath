import sys
from src.data_loader import load_challenge_data
from src.routing import solve_missions
from src.visualize import plot_solution

def run_pipeline():
    """
    Main pipeline for the NextEra Drone Challenge.
    """
    try:
        # 1. Load Data
        data = load_challenge_data()
        
        # 2. Solve Routing
        # 'missions' is a list of lists, where each sublist
        # is the sequence of *stops* (waypoint indices)
        missions = solve_missions(data)
        
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