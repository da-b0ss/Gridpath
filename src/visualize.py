import plotly.graph_objects as go
from src import config
from src.path_decoder import reconstruct_path

def plot_solution(missions: list[list[int]], data: dict):
    """
    Generates an interactive HTML map of the solved missions.
    """
    print("Generating visualization...")
    fig = go.Figure()
    all_coords = data['points_lat_long']
    predecessors = data['predecessors']

    # 1. Add the flight polygon boundary
    poly_lons, poly_lats = data['polygon'].exterior.coords.xy
    fig.add_trace(go.Scattermapbox(
        mode="lines",
        lon=list(poly_lons),
        lat=list(poly_lats),
        fill="toself",
        fillcolor="rgba(255, 0, 0, 0.1)",
        line=dict(color="red", width=2),
        name="Flight Zone"
    ))

    # 2. Add each mission as a full, detailed path
    all_mission_lons = []
    all_mission_lats = []
    
    for i, mission_stops in enumerate(missions):
        # Reconstruct the full path for each leg
        full_mission_path_indices = []
        for j in range(len(mission_stops) - 1):
            start_wp = mission_stops[j]
            end_wp = mission_stops[j+1]
            
            leg_path = reconstruct_path(start_wp, end_wp, predecessors)
            
            # Add all points *except* the last one
            # to avoid duplicates on the next leg
            full_mission_path_indices.extend(leg_path[:-1])
        
        full_mission_path_indices.append(mission_stops[-1])
        
        # Ensure indices are within bounds
        valid_indices = [idx for idx in full_mission_path_indices if idx < len(all_coords)]
        coords = all_coords[valid_indices]
        
        all_mission_lons.extend(coords[:, 0]) # lon is index 0
        all_mission_lats.extend(coords[:, 1]) # lat is index 1
        
        # Add a 'None' to break the line between missions
        all_mission_lons.append(None)
        all_mission_lats.append(None)

    fig.add_trace(go.Scattermapbox(
        mode="lines",
        lon=all_mission_lons,
        lat=all_mission_lats,
        line=dict(color="blue", width=2),
        name="Drone Missions"
    ))

    # 3. Configure layout and save
    center_lon, center_lat = data['polygon'].centroid.xy
    fig.update_layout(
        title="NextEra Drone Mission Plan",
        mapbox_style=config.MAPBOX_STYLE,
        mapbox_center_lon=center_lon[0],
        mapbox_center_lat=center_lat[0],
        mapbox_zoom=10,
        margin={"r":0,"t":40,"l":0,"b":0},
    )
    
    fig.write_html(config.OUTPUT_MAP_FILE)
    print(f"Success! Map saved to {config.OUTPUT_MAP_FILE}")