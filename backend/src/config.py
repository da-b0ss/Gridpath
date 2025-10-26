from pathlib import Path

# --- File Paths ---
# Path(__file__) is this config.py file
# .resolve() makes it an absolute path
# .parent is the 'src' directory
# .parent.parent is the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data"

# --- File Names ---
DISTANCE_MATRIX_FILE = DATA_PATH / "distance_matrix.npy"
PREDECESSORS_FILE = DATA_PATH / "predecessors.npy"
POINTS_LAT_LONG_FILE = DATA_PATH / "points_lat_long.npy"
ASSET_INDEXES_FILE = DATA_PATH / "asset_indexes.npy"
PHOTO_INDEXES_FILE = DATA_PATH / "photo_indexes.npy"
POLYGON_WKT_FILE = DATA_PATH / "polygon_lon_lat.wkt"

# --- Routing Parameters ---
DEPOT_INDEX = 0
MAX_MISSION_DISTANCE_FEET = 37725
# High number so the solver can use as many as needed
NUM_VEHICLES = 30 

# --- Visualization ---
OUTPUT_MAP_FILE = PROJECT_ROOT / ".." / "frontend" / "public" / "drone_missions_map.html"
MAPBOX_STYLE = "open-street-map"