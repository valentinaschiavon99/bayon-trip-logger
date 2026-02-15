import streamlit as st
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ingest import load_raw_csv
from features import add_dynamics, calculate_trip_metrics
from visualization import create_trip_map, create_acceleration_heatmap
from premium import PremiumTier
from ai_insights import classify_driving_style, generate_recommendations, detect_anomalies
from streamlit_folium import st_folium

st.set_page_config(page_title="🚗 Bayon Trip Logger", layout="wide", page_icon="🚗")

# Initialize premium tier
if 'premium' not in st.session_state:
    st.session_state.premium = False

# Sidebar for premium toggle
with st.sidebar:
    st.title("🚗 Bayon Trip Logger")
    st.markdown("---")
    
    # Premium toggle
    st.subheader("Account Type")
    premium_enabled = st.checkbox("Enable Premium Features 🌟", value=st.session_state.premium)
    st.session_state.premium = premium_enabled
    
    if premium_enabled:
        st.success("✅ Premium Mode Active")
        st.markdown("""
        **Premium Features Unlocked:**
        - 🎯 AI Driving Style Analysis
        - 📊 Advanced Analytics
        - 🗺️ Acceleration Heatmap
        - 💡 Personalized Recommendations
        - 📄 Export Capabilities
        """)
    else:
        st.info("ℹ️ Free Mode")
        st.markdown("""
        **Available Features:**
        - 📈 Basic Trip Metrics
        - 🗺️ Route Visualization
        
        **Upgrade to Premium for:**
        - 🎯 AI Insights
        - 📊 Advanced Analytics
        - 🗺️ Acceleration Heatmaps
        - And more!
        """)
    
    st.markdown("---")
    st.caption("Built with ❤️ using Streamlit")

# Initialize premium tier object
tier = PremiumTier(is_premium=st.session_state.premium)

# Main content
st.title("🚗 Bayon Trip Logger")
st.markdown("Personal driving analytics dashboard - Track, analyze, and improve your driving!")

# File upload
st.subheader("📂 Upload Trip Data")
uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])

if uploaded_file is not None:
    try:
        # Load and process data
        with st.spinner("Processing trip data..."):
            df = load_raw_csv(uploaded_file)
            df = add_dynamics(df)
            metrics = calculate_trip_metrics(df)
        
        st.success(f"✅ Loaded {len(df)} GPS points")
        
        # Display basic metrics (FREE)
        st.subheader("📊 Trip Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Duration", f"{metrics['duration_min']:.1f} min")
        with col2:
            st.metric("Distance", f"{metrics['distance_km']:.2f} km")
        with col3:
            st.metric("Avg Speed", f"{metrics['avg_speed_kmh']:.1f} km/h")
        with col4:
            st.metric("Max Speed", f"{metrics['max_speed_kmh']:.1f} km/h")
        
        # Smoothness score (FREE)
        st.subheader("🎯 Driving Smoothness Score")
        col1, col2 = st.columns([1, 3])
        with col1:
            score = metrics['smoothness_score']
            color = "green" if score >= 80 else "orange" if score >= 60 else "red"
            st.markdown(f"<h1 style='text-align: center; color: {color};'>{score:.1f}/100</h1>", 
                       unsafe_allow_html=True)
        with col2:
            st.markdown("""
            **Smoothness Score** measures how gently you accelerate and brake.
            - 🟢 **80-100**: Excellent - Very smooth driving
            - 🟡 **60-79**: Good - Some room for improvement
            - 🔴 **0-59**: Needs improvement - Consider smoother driving
            """)
        
        # Route map (FREE)
        st.subheader("🗺️ Route Map")
        trip_map = create_trip_map(df)
        if trip_map:
            st_folium(trip_map, width=1200, height=500)
        
        # PREMIUM FEATURES
        if tier.has_feature("ai_insights"):
            st.markdown("---")
            st.subheader("🌟 AI-Powered Insights (Premium)")
            
            # Driving style classification
            style, confidence = classify_driving_style(df)
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f"### Your Driving Style")
                st.markdown(f"<h2 style='text-align: center;'>{style}</h2>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center;'>Confidence: {confidence*100:.0f}%</p>", 
                           unsafe_allow_html=True)
            
            with col2:
                st.markdown("### 💡 Personalized Recommendations")
                recommendations = generate_recommendations(df, style)
                for rec in recommendations:
                    st.markdown(f"- {rec}")
            
            # Anomaly detection
            anomalies = detect_anomalies(df)
            if anomalies:
                st.warning("⚠️ **Anomalies Detected:**")
                for anomaly in anomalies:
                    st.markdown(f"- {anomaly}")
        
        if tier.has_feature("advanced_analytics"):
            st.markdown("---")
            st.subheader("📊 Advanced Analytics (Premium)")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Max Acceleration", f"{metrics['max_acceleration']:.2f} m/s²")
            with col2:
                st.metric("Max Deceleration", f"{metrics['max_deceleration']:.2f} m/s²")
            with col3:
                st.metric("Avg Jerk", f"{metrics['avg_jerk']:.2f} m/s³")
            
            st.markdown("""
            **Jerk** measures how smoothly you change acceleration. Lower values indicate smoother transitions.
            """)
        
        if tier.has_feature("acceleration_heatmap"):
            st.markdown("---")
            st.subheader("🔥 Acceleration Heatmap (Premium)")
            st.markdown("Red areas indicate high acceleration/braking, green areas indicate smooth driving")
            
            heatmap = create_acceleration_heatmap(df)
            if heatmap:
                st_folium(heatmap, width=1200, height=500)
        
        if tier.has_feature("export_data"):
            st.markdown("---")
            st.subheader("💾 Export Options (Premium)")
            
            col1, col2 = st.columns(2)
            with col1:
                # Export processed CSV
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Processed Data (CSV)",
                    data=csv,
                    file_name="processed_trip.csv",
                    mime="text/csv"
                )
            
            with col2:
                # Export metrics as JSON
                import json
                metrics_json = json.dumps(metrics, indent=2, default=str)
                st.download_button(
                    label="📥 Download Metrics (JSON)",
                    data=metrics_json,
                    file_name="trip_metrics.json",
                    mime="application/json"
                )
        
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        st.exception(e)

else:
    # Show sample format
    st.info("👆 Upload a CSV file to get started!")
    
    st.subheader("📋 Expected CSV Format")
    st.code("""timestamp,lat,lon,speed_mps,accuracy_m
2026-02-15T12:00:00+01:00,46.62,14.30,0.0,5
2026-02-15T12:00:05+01:00,46.62,14.30,5.5,5
2026-02-15T12:00:10+01:00,46.62,14.31,11.0,4
...""")
    
    st.markdown("""
    **Required columns:**
    - `timestamp`: ISO format datetime
    - `lat`: Latitude (WGS84)
    - `lon`: Longitude (WGS84)
    - `speed_mps`: Speed in meters per second
    - `accuracy_m`: GPS accuracy in meters (optional, but recommended)
    """)