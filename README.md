# 🚗 Bayon Trip Logger

Personal driving analytics dashboard built with Python & Streamlit.

## 📖 Overview

Bayon Trip Logger is a comprehensive driving analysis tool that processes trip data
(GPS position, speed, timestamps) and generates:

- Speed metrics (average / max)
- Driving smoothness score
- Interactive trip visualization
- AI-powered driving style insights (Premium)
- Advanced analytics and heatmaps (Premium)

Designed as a personal data analytics & AI experimentation project.

---

## ⚙️ Tech Stack

- Python
- Streamlit
- Pandas / NumPy
- Folium (maps)
- AI-powered insights

---

## 🚀 Features

### Free Tier ✅
- 📈 **Basic Trip Metrics**: Duration, distance, average/max speed
- 🎯 **Driving Smoothness Score**: 0-100 score based on acceleration smoothness
- 🗺️ **Route Visualization**: Interactive map with start/end markers
- 📂 **CSV Data Import**: Easy file upload for trip data

### Premium Tier 🌟
- 🎯 **AI Driving Style Analysis**: Classify your driving style (Eco-Friendly, Smooth, Sporty, Aggressive, Normal)
- 💡 **Personalized Recommendations**: Get actionable tips to improve your driving
- 📊 **Advanced Analytics**: Detailed acceleration, deceleration, and jerk metrics
- 🔥 **Acceleration Heatmap**: Visual heatmap showing acceleration patterns on the route
- 💾 **Export Capabilities**: Download processed data (CSV) and metrics (JSON)
- ⚠️ **Anomaly Detection**: Identify unusual driving patterns and potential GPS errors

---

## 📊 Feature Comparison

| Feature | Free | Premium |
|---------|------|---------|
| Basic Trip Metrics | ✅ | ✅ |
| Smoothness Score | ✅ | ✅ |
| Route Map | ✅ | ✅ |
| AI Driving Style Classification | ❌ | ✅ |
| Personalized Recommendations | ❌ | ✅ |
| Advanced Analytics | ❌ | ✅ |
| Acceleration Heatmap | ❌ | ✅ |
| Export Options | ❌ | ✅ |
| Anomaly Detection | ❌ | ✅ |

---

## 🚀 Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/valentinaschiavon99/bayon-trip-logger.git
cd bayon-trip-logger

# Install dependencies
pip install -r requirements.txt
```

### Running the App

```bash
# Start the Streamlit dashboard
streamlit run app/dashboard.py
```

The app will open in your browser at `http://localhost:8501`

### Enabling Premium Features

Toggle the "Enable Premium Features 🌟" checkbox in the sidebar to unlock all premium functionality.

---

## 📂 Expected CSV Format

```csv
timestamp,lat,lon,speed_mps,accuracy_m
2026-02-15T12:00:00+01:00,46.62,14.30,0.0,5
2026-02-15T12:00:05+01:00,46.62,14.30,5.5,5
2026-02-15T12:00:10+01:00,46.62,14.31,11.0,4
...
```

**Required columns:**
- `timestamp`: ISO format datetime (with timezone)
- `lat`: Latitude in decimal degrees (WGS84)
- `lon`: Longitude in decimal degrees (WGS84)
- `speed_mps`: Speed in meters per second
- `accuracy_m`: GPS accuracy in meters (optional, but recommended - filters out inaccurate readings)

---

## 🎯 How It Works

1. **Data Ingestion**: Upload your trip CSV file
2. **Data Processing**: Automatic cleaning, sorting, and filtering
3. **Feature Calculation**: Computes acceleration, jerk, and smoothness metrics
4. **Visualization**: Interactive maps and analytics dashboards
5. **AI Analysis** (Premium): Classifies driving style and generates recommendations

---

## 📸 Screenshots

### Free Mode
![Free Mode](https://github.com/user-attachments/assets/5a0ff73b-2826-459a-b695-81ce87929df4)
*Basic trip metrics, smoothness score, and route visualization*

### Free Mode with Data
![Free Mode with Data](https://github.com/user-attachments/assets/29fa121f-0e42-405a-b409-51f69b1b6b2b)
*Trip summary showing duration, distance, speeds, and smoothness score*

### Premium Mode
![Premium Mode](https://github.com/user-attachments/assets/8d48bd47-5f51-425e-91eb-76f9f0bfd207)
*AI-powered insights, advanced analytics, acceleration heatmap, and export options*

---

## 🧪 Project Structure

```
bayon-trip-logger/
├── app/
│   └── dashboard.py        # Streamlit dashboard application
├── src/
│   ├── ingest.py          # CSV data loading and cleaning
│   ├── features.py        # Feature engineering (acceleration, jerk, metrics)
│   ├── premium.py         # Premium tier management
│   ├── ai_insights.py     # AI-powered driving style analysis
│   └── visualization.py   # Map and heatmap generation
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

---

## 🔒 Privacy & Data

- All data processing happens **locally** on your machine
- No data is sent to external servers
- Your trip data stays private

---

## 🛠️ Development

This project is designed for experimentation with:
- Data analytics pipelines
- Interactive visualizations
- AI/ML-based insights
- Streamlit dashboard development

---

## 📝 License

This is a personal project for learning and experimentation.

---

## 🤝 Contributing

This is a personal project, but suggestions and feedback are welcome!