import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from src import config

def view_distance_matrix():
    """View the distance matrix as a heatmap"""
    print("Loading distance matrix...")
    data = np.load(config.DISTANCE_MATRIX_FILE)
    print(f"Distance matrix shape: {data.shape}")
    print(f"Distance matrix dtype: {data.dtype}")
    print(f"Min distance: {data.min():.2f}")
    print(f"Max distance: {data.max():.2f}")
    print(f"Mean distance: {data.mean():.2f}")
    
    # Show a sample of the matrix
    # This function is not modified by the new_code, so it remains as is.
    # The new_code only added new functions for Plotly visualization.
    # The original matplotlib plot is kept.
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend
    import matplotlib.pyplot as plt
    
    plt.figure(figsize=(10, 8))
    plt.imshow(data[:100, :100], cmap='viridis')  # Show first 100x100 for visualization
    plt.colorbar(label='Distance (feet)')
    plt.title('Distance Matrix (first 100x100 points)')
    plt.xlabel('Waypoint Index')
    plt.ylabel('Waypoint Index')
    plt.savefig('distance_matrix_sample.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Distance matrix sample saved as 'distance_matrix_sample.png'")

def view_coordinates_plotly():
    """View the lat/long coordinates using Plotly"""
    print("Loading coordinates...")
    data = np.load(config.POINTS_LAT_LONG_FILE)
    print(f"Coordinates shape: {data.shape}")
    print(f"Longitude range: {data[:, 0].min():.6f} to {data[:, 0].max():.6f}")
    print(f"Latitude range: {data[:, 1].min():.6f} to {data[:, 1].max():.6f}")
    
    # Create Plotly figure
    fig = go.Figure()
    
    # Add all waypoints
    fig.add_trace(go.Scattermapbox(
        mode="markers",
        lon=data[:, 0],
        lat=data[:, 1],
        marker=dict(size=3, color="blue", opacity=0.6),
        name="All Waypoints",
        text=[f"Waypoint {i}" for i in range(len(data))],
        hovertemplate="<b>%{text}</b><br>Lon: %{lon:.6f}<br>Lat: %{lat:.6f}<extra></extra>"
    ))
    
    # Configure layout
    center_lon = data[:, 0].mean()
    center_lat = data[:, 1].mean()
    
    fig.update_layout(
        title="All Waypoints",
        mapbox_style="open-street-map",
        mapbox_center_lon=center_lon,
        mapbox_center_lat=center_lat,
        mapbox_zoom=10,
        margin={"r":0,"t":40,"l":0,"b":0},
        height=600
    )
    
    fig.write_html("waypoints_plotly.html")
    print("Waypoints map saved as 'waypoints_plotly.html'")

def view_index_ranges():
    """View the asset and photo index ranges"""
    print("Loading index ranges...")
    
    # Asset indexes
    asset_slice = np.load(config.ASSET_INDEXES_FILE)
    print(f"Asset indexes: {asset_slice[0]} to {asset_slice[1]} (total: {asset_slice[1] - asset_slice[0] + 1})")
    
    # Photo indexes  
    photo_slice = np.load(config.PHOTO_INDEXES_FILE)
    print(f"Photo indexes: {photo_slice[0]} to {photo_slice[1]} (total: {photo_slice[1] - photo_slice[0] + 1})")
    
    # Waypoint indexes
    waypoint_slice = np.load(config.DATA_PATH / "waypoint_indexes.npy")
    print(f"Waypoint indexes: {waypoint_slice[0]} to {waypoint_slice[1]} (total: {waypoint_slice[1] - waypoint_slice[0] + 1})")

def view_predecessors():
    """View the predecessors matrix"""
    print("Loading predecessors matrix...")
    data = np.load(config.PREDECESSORS_FILE)
    print(f"Predecessors shape: {data.shape}")
    print(f"Predecessors dtype: {data.dtype}")
    print(f"Unique values: {len(np.unique(data))}")
    print(f"Min value: {data.min()}")
    print(f"Max value: {data.max()}")
    
    # Show a sample
    print("\nSample predecessor values:")
    print(data[:5, :5])

def view_polygon_plotly():
    """View the flight zone polygon using Plotly"""
    print("Loading flight zone polygon...")
    from shapely import wkt
    
    with open(config.POLYGON_WKT_FILE, 'r') as f:
        polygon_wkt = f.read()
    
    polygon = wkt.loads(polygon_wkt)
    print(f"Polygon type: {type(polygon)}")
    print(f"Polygon bounds: {polygon.bounds}")
    print(f"Polygon area: {polygon.area:.6f}")
    
    # Create Plotly figure
    fig = go.Figure()
    
    # Add polygon boundary
    x, y = polygon.exterior.xy
    fig.add_trace(go.Scattermapbox(
        mode="lines",
        lon=list(x),
        lat=list(y),
        fill="toself",
        fillcolor="rgba(255, 0, 0, 0.2)",
        line=dict(color="red", width=3),
        name="Flight Zone",
        hovertemplate="<b>Flight Zone Boundary</b><extra></extra>"
    ))
    
    # Configure layout
    center_lon = (polygon.bounds[0] + polygon.bounds[2]) / 2
    center_lat = (polygon.bounds[1] + polygon.bounds[3]) / 2
    
    fig.update_layout(
        title="Flight Zone Polygon",
        mapbox_style="open-street-map",
        mapbox_center_lon=center_lon,
        mapbox_center_lat=center_lat,
        mapbox_zoom=10,
        margin={"r":0,"t":40,"l":0,"b":0},
        height=600
    )
    
    fig.write_html("flight_zone_plotly.html")
    print("Flight zone polygon saved as 'flight_zone_plotly.html'")

def view_combined_plotly():
    """View both waypoints and polygon together"""
    print("Loading combined view...")
    
    # Load coordinates
    coords_data = np.load(config.POINTS_LAT_LONG_FILE)
    
    # Load polygon
    from shapely import wkt
    with open(config.POLYGON_WKT_FILE, 'r') as f:
        polygon_wkt = f.read()
    polygon = wkt.loads(polygon_wkt)
    
    # Create Plotly figure
    fig = go.Figure()
    
    # Add polygon
    x, y = polygon.exterior.xy
    fig.add_trace(go.Scattermapbox(
        mode="lines",
        lon=list(x),
        lat=list(y),
        fill="toself",
        fillcolor="rgba(255, 0, 0, 0.1)",
        line=dict(color="red", width=2),
        name="Flight Zone"
    ))
    
    # Add waypoints
    fig.add_trace(go.Scattermapbox(
        mode="markers",
        lon=coords_data[:, 0],
        lat=coords_data[:, 1],
        marker=dict(size=2, color="blue", opacity=0.7),
        name="Waypoints",
        text=[f"WP {i}" for i in range(len(coords_data))],
        hovertemplate="<b>%{text}</b><br>Lon: %{lon:.6f}<br>Lat: %{lat:.6f}<extra></extra>"
    ))
    
    # Configure layout
    center_lon = coords_data[:, 0].mean()
    center_lat = coords_data[:, 1].mean()
    
    fig.update_layout(
        title="Flight Zone and Waypoints",
        mapbox_style="open-street-map",
        mapbox_center_lon=center_lon,
        mapbox_center_lat=center_lat,
        mapbox_zoom=10,
        margin={"r":0,"t":40,"l":0,"b":0},
        height=700
    )
    
    fig.write_html("combined_view_plotly.html")
    print("Combined view saved as 'combined_view_plotly.html'")

def main():
    """Main function to view all data with Plotly"""
    print("=== NextEra Drone Challenge Data Viewer (Plotly) ===\n")
    
    try:
        print("1. Distance Matrix:")
        view_distance_matrix()
        print("\n" + "="*50 + "\n")
        
        print("2. Coordinates:")
        view_coordinates_plotly()
        print("\n" + "="*50 + "\n")
        
        print("3. Index Ranges:")
        view_index_ranges()
        print("\n" + "="*50 + "\n")
        
        print("4. Predecessors Matrix:")
        view_predecessors()
        print("\n" + "="*50 + "\n")
        
        print("5. Flight Zone Polygon:")
        view_polygon_plotly()
        print("\n" + "="*50 + "\n")
        
        print("6. Combined View:")
        view_combined_plotly()
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure all data files are present and dependencies are installed.")

if __name__ == "__main__":
    main()