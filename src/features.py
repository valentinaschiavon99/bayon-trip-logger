import numpy as np

def add_dynamics(df):
    df = df.copy()

    dt = df["timestamp"].diff().dt.total_seconds()
    df["dt_s"] = dt.fillna(0).clip(lower=0)

    dv = df["speed_mps"].diff().fillna(0)
    dt_safe = df["dt_s"].replace(0, np.nan)

    df["acc_mps2"] = (dv / dt_safe).fillna(0).clip(-10, 10)

    da = df["acc_mps2"].diff().fillna(0)
    df["jerk_mps3"] = (da / dt_safe).fillna(0).clip(-20, 20)

    return df

def calculate_smoothness_score(df):
    """
    Calculate a driving smoothness score (0-100).
    Higher score = smoother driving (lower acceleration/jerk variations).
    """
    if len(df) < 2:
        return 100.0
    
    # Calculate metrics
    acc_std = df["acc_mps2"].std()
    jerk_std = df["jerk_mps3"].std()
    
    # Normalize (typical good driving: acc_std < 1, jerk_std < 2)
    acc_penalty = min(acc_std / 1.0, 1.0) * 50
    jerk_penalty = min(jerk_std / 2.0, 1.0) * 50
    
    score = 100 - acc_penalty - jerk_penalty
    return max(0, min(100, score))

def calculate_trip_metrics(df):
    """Calculate comprehensive trip metrics."""
    metrics = {
        "duration_min": (df["timestamp"].max() - df["timestamp"].min()).total_seconds() / 60,
        "distance_km": (df["speed_mps"] * df["dt_s"]).sum() / 1000,
        "avg_speed_kmh": df["speed_kmh"].mean(),
        "max_speed_kmh": df["speed_kmh"].max(),
        "smoothness_score": calculate_smoothness_score(df),
        "max_acceleration": df["acc_mps2"].max(),
        "max_deceleration": df["acc_mps2"].min(),
        "avg_jerk": df["jerk_mps3"].abs().mean(),
    }
    return metrics