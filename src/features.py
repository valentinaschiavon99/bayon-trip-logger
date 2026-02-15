import numpy as np

def add_dynamics(df):
    df = df.copy()

    dt = df["timestamp"].diff().dt.total_seconds()
    df["dt_s"] = dt.fillna(0).clip(lower=0)

    dv = df["speed_mps"].diff().fillna(0)
    dt_safe = df["dt_s"].replace(0, np.nan)

    df["acc_mps2"] = (dv / dt_safe).fillna(0).clip(-10, 10)

    da =