from typing import Dict, Any
import numpy as np
import pandas as pd

# Physical limits for clipping unrealistic values
MAX_ACCELERATION_MPS2 = 10.0  # ~1g
MIN_ACCELERATION_MPS2 = -10.0  # ~-1g
MAX_JERK_MPS3 = 20.0
MIN_JERK_MPS3 = -20.0

# Smoothness scoring thresholds
GOOD_DRIVING_ACC_STD = 1.0  # m/s² std deviation
GOOD_DRIVING_JERK_STD = 2.0  # m/s³ std deviation
SMOOTHNESS_MAX_SCORE = 100.0
SMOOTHNESS_ACC_WEIGHT = 50.0
SMOOTHNESS_JERK_WEIGHT = 50.0


def add_dynamics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add dynamic motion features to trip data.

    Calculates time deltas, acceleration, and jerk from speed and timestamp data.

    Args:
        df: DataFrame with 'timestamp' and 'speed_mps' columns

    Returns:
        DataFrame with added columns: 'dt_s', 'acc_mps2', 'jerk_mps3'

    Raises:
        ValueError: If required columns are missing
    """
    required_cols = ["timestamp", "speed_mps"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    if len(df) == 0:
        return df.copy()

    df = df.copy()

    # Calculate time deltas
    dt = df["timestamp"].diff().dt.total_seconds()
    df["dt_s"] = dt.fillna(0).clip(lower=0)

    # Calculate acceleration
    dv = df["speed_mps"].diff().fillna(0)
    dt_safe = df["dt_s"].replace(0, np.nan)
    df["acc_mps2"] = (dv / dt_safe).fillna(0).clip(MIN_ACCELERATION_MPS2, MAX_ACCELERATION_MPS2)

    # Calculate jerk (rate of change of acceleration)
    da = df["acc_mps2"].diff().fillna(0)
    df["jerk_mps3"] = (da / dt_safe).fillna(0).clip(MIN_JERK_MPS3, MAX_JERK_MPS3)

    return df


def calculate_smoothness_score(df: pd.DataFrame) -> float:
    """
    Calculate a driving smoothness score (0-100).

    Higher score indicates smoother driving with less variation in acceleration
    and jerk. Score is based on standard deviations compared to good driving thresholds.

    Args:
        df: DataFrame with 'acc_mps2' and 'jerk_mps3' columns

    Returns:
        Smoothness score between 0 and 100

    Raises:
        ValueError: If required columns are missing
    """
    required_cols = ["acc_mps2", "jerk_mps3"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    if len(df) < 2:
        return SMOOTHNESS_MAX_SCORE

    # Calculate variation in acceleration and jerk
    acc_std = df["acc_mps2"].std()
    jerk_std = df["jerk_mps3"].std()

    # Calculate penalties normalized against good driving thresholds
    acc_penalty = min(acc_std / GOOD_DRIVING_ACC_STD, 1.0) * SMOOTHNESS_ACC_WEIGHT
    jerk_penalty = min(jerk_std / GOOD_DRIVING_JERK_STD, 1.0) * SMOOTHNESS_JERK_WEIGHT

    score = SMOOTHNESS_MAX_SCORE - acc_penalty - jerk_penalty
    return max(0, min(SMOOTHNESS_MAX_SCORE, score))


def calculate_trip_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate comprehensive trip metrics from GPS data.

    Args:
        df: DataFrame with columns: 'timestamp', 'speed_mps', 'speed_kmh',
            'dt_s', 'acc_mps2', 'jerk_mps3'

    Returns:
        Dictionary containing:
            - duration_min: Trip duration in minutes
            - distance_km: Total distance traveled in kilometers
            - avg_speed_kmh: Average speed in km/h
            - max_speed_kmh: Maximum speed in km/h
            - smoothness_score: Driving smoothness (0-100)
            - max_acceleration: Maximum acceleration in m/s²
            - max_deceleration: Maximum deceleration (most negative) in m/s²
            - avg_jerk: Average absolute jerk in m/s³

    Raises:
        ValueError: If required columns are missing or DataFrame is empty
    """
    required_cols = ["timestamp", "speed_mps", "speed_kmh", "dt_s", "acc_mps2", "jerk_mps3"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    if len(df) == 0:
        raise ValueError("Cannot calculate metrics for empty DataFrame")

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