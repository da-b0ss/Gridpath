# Project Explanation

## Pipeline Overview

The pipeline is designed to address the NextEra Energy Drone Optimization Challenge by automating the process of planning and visualizing efficient drone missions. It adheres to the constraints and assumptions outlined in the guide, ensuring full coverage of required waypoints while respecting battery limits and airspace boundaries.

---

## How Each File Contributes

### 1. `src/config.py`
- **Purpose**: Centralizes file paths and parameters for easy access across modules.
- **Key Features**:
  - Defines paths to input data files (`distance_matrix.npy`, `predecessors.npy`, etc.).
  - Stores routing parameters like `DEPOT_INDEX` and `MAX_MISSION_DISTANCE_FEET`.
  - Specifies visualization settings (e.g., `MAPBOX_STYLE`).
- **Why It's Important**:
  - Ensures consistency and reduces hardcoding, making the pipeline modular and maintainable.

---

### 2. `src/data_loader.py`
- **Purpose**: Loads and preprocesses input data files.
- **Key Features**:
  - Reads `.npy` and `.wkt` files using `numpy` and `shapely`.
  - Filters out-of-bounds indices defensively, as suggested in the guide.
  - Prepares a dictionary of data for use in routing and visualization.
- **Why It's Important**:
  - Ensures all data is correctly loaded and validated, preventing runtime errors in subsequent steps.

---

### 3. `src/routing.py`
- **Purpose**: Solves the Capacitated Vehicle Routing Problem (CVRP) using Google OR-Tools.
- **Key Features**:
  - Constructs a smaller distance matrix for required waypoints.
  - Implements constraints like maximum mission distance (`MAX_MISSION_DISTANCE_FEET`).
  - Uses OR-Tools to compute optimal routes for drones.
- **Why It's Important**:
  - Finds efficient routes that minimize total distance while respecting constraints, addressing the core challenge.

---

### 4. `src/path_decoder.py`
- **Purpose**: Reconstructs detailed paths from the predecessor matrix.
- **Key Features**:
  - Implements Dijkstra-style path reconstruction using `predecessors.npy`.
  - Handles cases where no path exists gracefully.
- **Why It's Important**:
  - Converts abstract routes into detailed waypoint sequences, ensuring missions respect airspace boundaries.

---

### 5. `src/visualize.py`
- **Purpose**: Generates an interactive map of the solved missions.
- **Key Features**:
  - Plots the flight zone polygon using `polygon_lon_lat.wkt`.
  - Visualizes detailed mission paths using `points_lat_long.npy`.
  - Saves the map as an HTML file for easy sharing and review.
- **Why It's Important**:
  - Provides a clear, visual representation of the solution, making it easy to validate and present.

---

### 6. `main.py`
- **Purpose**: Orchestrates the pipeline.
- **Key Features**:
  - Calls `load_challenge_data()` to load data.
  - Passes the data to `solve_missions()` to compute routes.
  - Sends the routes and data to `plot_solution()` to generate the map.
- **Why It's Important**:
  - Serves as the entry point for the pipeline, ensuring all steps are executed in sequence.

---

## How This Solves the Problem

### 1. Full Coverage
- The pipeline ensures all required photo waypoints are visited at least once, as mandated by the challenge.

### 2. Constraint Handling
- Battery limits are respected by splitting routes into missions that stay under the maximum allowed distance (`37,725 feet`).
- Airspace boundaries are enforced by using the `distance_matrix.npy` and `predecessors.npy` files.

### 3. Efficiency
- The routing logic minimizes total distance traveled, reducing operational costs.

### 4. Visualization
- The interactive map provides clear evidence of coverage and constraint handling, meeting the challenge's deliverable requirements.

---

## Why This Approach Was Chosen

### Modular Design
- Each step is handled by a separate module, making the pipeline easy to maintain and extend.

### Validation
- Defensive checks ensure indices are within bounds, preventing runtime errors.

### Scalability
- The pipeline can handle different datasets and parameters without modification.

### Visualization
- The interactive map provides a user-friendly way to review the solution.

---

## How It Aligns with the Guide

### Suggested Workflow
1. **Inspect the Data**:
   - The pipeline loads and validates all input files.
2. **Build an Unconstrained Tour**:
   - The routing logic solves the CVRP using OR-Tools.
3. **Decode Real Paths**:
   - The path decoder reconstructs detailed waypoint sequences.
4. **Respect Battery Limits**:
   - Missions are split to stay under the maximum allowed distance.
5. **Convert to Coordinates**:
   - Waypoint indices are mapped to longitude/latitude for visualization.
6. **Visualize and Validate**:
   - The map overlays missions on the flight zone, ensuring all constraints are respected.

---

Let me know if you need further clarification or additional details!