"""AI-powered insights for premium users."""
import numpy as np

def classify_driving_style(df):
    """
    Classify driving style based on trip metrics.
    Returns: style name and confidence score.
    """
    if len(df) < 10:
        return "Unknown", 0.0
    
    # Extract features
    acc_std = df["acc_mps2"].std()
    jerk_std = df["jerk_mps3"].std()
    max_acc = df["acc_mps2"].max()
    max_dec = abs(df["acc_mps2"].min())
    avg_speed = df["speed_kmh"].mean()
    
    # Simple rule-based classification (can be replaced with ML model)
    if acc_std < 0.5 and jerk_std < 1.0:
        return "🌿 Eco-Friendly", 0.92
    elif acc_std < 1.0 and jerk_std < 1.5:
        return "😌 Smooth", 0.88
    elif max_acc > 3.0 or max_dec > 3.0:
        return "🏎️ Sporty", 0.85
    elif acc_std > 2.0 or jerk_std > 3.0:
        return "⚡ Aggressive", 0.90
    else:
        return "🚗 Normal", 0.75

def generate_recommendations(df, driving_style):
    """Generate personalized driving recommendations."""
    recommendations = []
    
    acc_std = df["acc_mps2"].std()
    jerk_std = df["jerk_mps3"].std()
    max_speed = df["speed_kmh"].max()
    
    if acc_std > 1.5:
        recommendations.append("🎯 Try smoother acceleration to improve fuel efficiency")
    
    if jerk_std > 2.0:
        recommendations.append("🎯 Reduce sudden speed changes for better comfort")
    
    if max_speed > 120:
        recommendations.append("🎯 Consider maintaining moderate speeds for safety")
    
    # Count harsh events
    harsh_acc = (df["acc_mps2"] > 2.5).sum()
    harsh_brake = (df["acc_mps2"] < -2.5).sum()
    
    if harsh_acc > 0:
        recommendations.append(f"⚠️ {harsh_acc} harsh acceleration event(s) detected")
    
    if harsh_brake > 0:
        recommendations.append(f"⚠️ {harsh_brake} harsh braking event(s) detected")
    
    if not recommendations:
        recommendations.append("✅ Excellent driving! Keep up the good work!")
    
    return recommendations

def detect_anomalies(df):
    """Detect unusual patterns in driving data."""
    anomalies = []
    
    # Detect speed spikes
    speed_diff = df["speed_kmh"].diff().abs()
    if speed_diff.max() > 50:
        anomalies.append("⚠️ Sudden speed change detected (possible GPS error)")
    
    # Detect excessive acceleration
    if df["acc_mps2"].max() > 5:
        anomalies.append("⚠️ Extremely high acceleration detected")
    
    # Detect excessive braking
    if df["acc_mps2"].min() < -5:
        anomalies.append("⚠️ Extremely hard braking detected")
    
    return anomalies
