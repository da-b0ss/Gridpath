import plotly.graph_objects as go
from src import config
from src.path_decoder import reconstruct_path

def plot_solution(missions: list[list[int]], data: dict):
    """
    Generates an interactive HTML map of the solved missions.
    """
    print("Generating visualization...")
    
    # === COVERAGE VERIFICATION ===
    required_waypoints = set(data['required_waypoints'])
    visited_waypoints = set()
    
    # Collect all visited waypoints from missions
    print("MISSION DATA", len(missions))
    for mission in missions:
        for waypoint in mission:
            if waypoint in required_waypoints:
                visited_waypoints.add(waypoint)
    
    # Calculate coverage statistics
    coverage_percentage = (len(visited_waypoints) / len(required_waypoints)) * 100
    missing_waypoints = required_waypoints - visited_waypoints
    
    print(f"Coverage Analysis:")
    print(f"  Required waypoints: {len(required_waypoints)}")
    print(f"  Visited waypoints: {len(visited_waypoints)}")
    print(f"  Coverage: {coverage_percentage:.1f}%")
    if missing_waypoints:
        print(f"  Missing waypoints: {len(missing_waypoints)}")
    
    # === CONTINUE WITH EXISTING CODE ===
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

    # 2. Add required waypoints (photo points that must be visited)
    required_coords = all_coords[list(required_waypoints)]
    fig.add_trace(go.Scattermapbox(
        mode="markers",
        lon=required_coords[:, 0],
        lat=required_coords[:, 1],
        marker=dict(size=6, color="orange", opacity=0.8),
        name=f"Required Waypoints ({len(required_waypoints)})",
        text=[f"Required {i}" for i in required_waypoints],
        hovertemplate="<b>%{text}</b><br>Lon: %{lon:.6f}<br>Lat: %{lat:.6f}<extra></extra>"
    ))

    # 2.5. Add asset waypoints (electrical poles - for visual aid only)
    asset_indices = data['asset_indices']
    if asset_indices:
        asset_coords = all_coords[asset_indices]
        fig.add_trace(go.Scattermapbox(
            mode="markers",
            lon=asset_coords[:, 0],
            lat=asset_coords[:, 1],
            marker=dict(size=4, color="purple", opacity=0.6),
            name=f"Assets/Poles ({len(asset_indices)})",
            text=[f"Asset {i}" for i in asset_indices],
            hovertemplate="<b>%{text}</b><br>Lon: %{lon:.6f}<br>Lat: %{lat:.6f}<extra></extra>"
        ))

    # 3. Add missing waypoints (if any) as red dots
    if missing_waypoints:
        missing_coords = all_coords[list(missing_waypoints)]
        fig.add_trace(go.Scattermapbox(
            mode="markers",
            lon=missing_coords[:, 0],
            lat=missing_coords[:, 1],
            marker=dict(size=8, color="red"),
            name=f"Missing Waypoints ({len(missing_waypoints)})",
            text=[f"Missing {i}" for i in missing_waypoints],
            hovertemplate="<b>%{text}</b><br>Lon: %{lon:.6f}<br>Lat: %{lat:.6f}<extra></extra>"
        ))

    # 4. Add each mission as a full, detailed path with different colors
    mission_colors = [
        'blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray', 
        'olive', 'cyan', 'magenta', 'lime', 'indigo', 'violet', 'gold',
        'darkblue', 'darkred', 'darkgreen', 'darkorange', 'darkviolet'
    ]
    
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
        
        # Get color for this mission (cycle through colors if more missions than colors)
        mission_color = mission_colors[i % len(mission_colors)]
        
        # Add this mission as a separate trace
        fig.add_trace(go.Scattermapbox(
            mode="lines",
            lon=coords[:, 0],
            lat=coords[:, 1],
            line=dict(color=mission_color, width=3),
            name=f"Mission {i+1}",
            hovertemplate=f"<b>Mission {i+1}</b><br>Step: %{{pointIndex}}<br>Lon: %{{lon}}<br>Lat: %{{lat}}<extra></extra>",
            showlegend=True
        ))

    # 5. Add depot (start/end point)
    depot_coords = all_coords[config.DEPOT_INDEX]
    fig.add_trace(go.Scattermapbox(
        mode="markers",
        lon=[depot_coords[0]],
        lat=[depot_coords[1]],
        marker=dict(size=10, color="green"),
        name="Depot (Start/End)",
        text=["Depot"],
        hovertemplate="<b>%{text}</b><br>Lon: %{lon:.6f}<br>Lat: %{lat:.6f}<extra></extra>"
    ))

    # 6. Configure layout and save
    center_lon, center_lat = data['polygon'].centroid.xy
    
    # Add coverage info to title
    title = f"NextEra Drone Mission Plan - Coverage: {coverage_percentage:.1f}%"
    if missing_waypoints:
        title += f" (Missing: {len(missing_waypoints)})"
    
    
    # Add coverage info to title
    title = f"NextEra Drone Mission Plan - Coverage: {coverage_percentage:.1f}%"
    if missing_waypoints:
        title += f" (Missing: {len(missing_waypoints)})"
    
    fig.update_layout(
        title=title,
        mapbox_style=config.MAPBOX_STYLE,
        mapbox_center_lon=center_lon[0],
        mapbox_center_lat=center_lat[0],
        mapbox_zoom=10,
        margin={"r":0,"t":40,"l":0,"b":0},
    )
    
    fig.write_html(config.OUTPUT_MAP_FILE)
    print(f"Success! Map saved to {config.OUTPUT_MAP_FILE}")
    
    # Return coverage statistics for further analysis
    return {
        'coverage_percentage': coverage_percentage,
        'total_required': len(required_waypoints),
        'total_visited': len(visited_waypoints),
        'missing_waypoints': list(missing_waypoints),
        'full_coverage': len(missing_waypoints) == 0
    }
    
    # Return coverage statistics for further analysis
    return {
        'coverage_percentage': coverage_percentage,
        'total_required': len(required_waypoints),
        'total_visited': len(visited_waypoints),
        'missing_waypoints': list(missing_waypoints),
        'full_coverage': len(missing_waypoints) == 0
    }