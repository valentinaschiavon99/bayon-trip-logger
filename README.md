# 🚗 Bayon Trip Logger

Personal driving analytics dashboard built with Python & Streamlit.

## 📖 Overview

Bayon Trip Logger is a lightweight driving analysis tool that processes trip data
(GPS position, speed, timestamps) and generates:

- Speed metrics (average / max)
- Driving smoothness score
- Interactive trip visualization

Designed as a personal data analytics & AI experimentation project.

---

## ⚙️ Tech Stack

- Python
- Streamlit
- Pandas / NumPy
- Folium (maps)
- Scikit-learn (future AI features)

---

## 🚀 Features

✅ Trip CSV ingestion  
✅ Speed calculations  
✅ Acceleration & jerk estimation  
✅ Smoothness score  
✅ Interactive map visualization  

---

## 📂 Expected CSV Format

```csv
timestamp,lat,lon,speed_mps,accuracy_m
2026-02-15T12:00:00+01:00,46.62,14.30,0.0,5