"""Visualization utilities for trip analysis."""
import folium
from folium import plugins
import pandas as pd

def create_trip_map(df):
    """Create an interactive map with the trip route."""
    if len(df) == 0:
        return None
    
    # Calculate center
    center_lat = df["lat"].mean()
    center_lon = df["lon"].mean()
    
    # Create map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=13,
        tiles='OpenStreetMap'
    )
    
    # Add route as polyline
    points = df[["lat", "lon"]].values.tolist()
    folium.PolyLine(
        points,
        color="blue",
        weight=3,
        opacity=0.7,
        popup="Trip Route"
    ).add_to(m)
    
    # Add start marker
    folium.Marker(
        location=[df.iloc[0]["lat"], df.iloc[0]["lon"]],
        popup="Start",
        icon=folium.Icon(color="green", icon="play")
    ).add_to(m)
    
    # Add end marker
    folium.Marker(
        location=[df.iloc[-1]["lat"], df.iloc[-1]["lon"]],
        popup="End",
        icon=folium.Icon(color="red", icon="stop")
    ).add_to(m)
    
    return m

def create_acceleration_heatmap(df):
    """Create a heatmap overlay showing acceleration intensity (premium feature)."""
    if len(df) == 0:
        return None
    
    center_lat = df["lat"].mean()
    center_lon = df["lon"].mean()
    
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=13,
        tiles='OpenStreetMap'
    )
    
    # Prepare heatmap data with acceleration intensity
    heat_data = []
    for _, row in df.iterrows():
        # Use absolute acceleration as intensity
        intensity = abs(row.get("acc_mps2", 0))
        # Normalize to 0-1 range for better visualization
        intensity = min(intensity / 5.0, 1.0)
        heat_data.append([row["lat"], row["lon"], intensity])
    
    # Add heatmap
    plugins.HeatMap(
        heat_data,
        min_opacity=0.2,
        max_opacity=0.8,
        radius=15,
        blur=20,
        gradient={0.0: 'green', 0.5: 'yellow', 1.0: 'red'}
    ).add_to(m)
    
    # Add route as polyline
    points = df[["lat", "lon"]].values.tolist()
    folium.PolyLine(
        points,
        color="blue",
        weight=2,
        opacity=0.4
    ).add_to(m)
    
    return m

def get_speed_color(speed_kmh):
    """Get color based on speed."""
    if speed_kmh < 30:
        return "green"
    elif speed_kmh < 60:
        return "yellow"
    elif speed_kmh < 90:
        return "orange"
    else:
        return "red"
