import pandas as pd

def load_raw_csv(path_or_buffer):
    df = pd.read_csv(path_or_buffer)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=False)
    df = df.sort_values("timestamp").reset_index(drop=True)

    df = df.dropna(subset=["lat", "lon", "speed_mps"])
    
    if "accuracy_m" in df.columns:
        df = df[df["accuracy_m"].fillna(9999) <= 100]

    df["speed_mps"] = df["speed_mps"].clip(lower=0)
    df["speed_kmh"] = df["speed_mps"] * 3.6

    return df