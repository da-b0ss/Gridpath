import numpy as np
from shapely import wkt
from src import config

def load_challenge_data():
    """Loads all data files from disk and returns them in a dict."""
    print("Loading data...")
    data = {}
    data['distance_matrix'] = np.load(config.DISTANCE_MATRIX_FILE)
    data['predecessors'] = np.load(config.PREDECESSORS_FILE)
    data['points_lat_long'] = np.load(config.POINTS_LAT_LONG_FILE)
    
    # Load and process the index slices
    asset_slice = np.load(config.ASSET_INDEXES_FILE)
    photo_slice = np.load(config.PHOTO_INDEXES_FILE)
    
    # Filter out-of-bounds indices per the "helpful hint"
    max_index = len(data['points_lat_long'])
    
    data['asset_indices'] = list(range(asset_slice[0], min(asset_slice[1] + 1, max_index)))
    
    # The photo indices are the *required* waypoints
    # Ensure the upper bound is strictly less than max_index
    photo_indices_raw = list(range(photo_slice[0], min(photo_slice[1], max_index - 1) + 1))
    
    # Ensure depot is not in the list of places to visit
    data['required_waypoints'] = [idx for idx in photo_indices_raw if idx != config.DEPOT_INDEX]
    
    # Load the flight polygon
    with open(config.POLYGON_WKT_FILE, 'r') as f:
        data['polygon'] = wkt.loads(f.read())
        
    print(f"Loaded {len(data['required_waypoints'])} required photo waypoints.")
    return data