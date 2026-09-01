# 🛡️ JunctionGuard AI — Autonomous Road Hazard Intelligence & Surveillance Platform

<div align="center">

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-00FFFF.svg?logo=yolo&logoColor=white)](https://ultralytics.com/)
[![Supabase](https://img.shields.io/badge/Supabase-Cloud_Storage_&_DB-3ECF8E.svg?logo=supabase&logoColor=white)](https://supabase.com/)
[![Render](https://img.shields.io/badge/Render-Live_Deployment-46E3B7.svg?logo=render&logoColor=white)](https://render.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests: 42 Passed](https://img.shields.io/badge/Tests-42%20Passed-brightgreen.svg)]()

**A production-grade, 100% explainable AI road safety surveillance suite engineered for Indian metropolitan corridors.**

[🚀 Open Live Web App](https://junctionguard-ai-jxn1.onrender.com) · [📑 Architecture Documentation](#-technical-architecture)

</div>

---

## 📖 Overview

**JunctionGuard AI** is an autonomous, explainable AI surveillance platform that continuously monitors and scores accident-prone road junctions across India. It fuses edge computer vision (**YOLOv8n + ByteTrack**), historical collision datasets (**MoRTH / OpenCity**), and crowdsourced citizen field evidence with cloud storage (**Supabase**) to generate transparent, deterministic risk scores for every urban node — enabling traffic authorities and city engineers to prevent collisions *proactively*.

> India records ~1.5 lakh road fatalities every year. JunctionGuard AI transforms passive camera streams and open telemetry into real-time, actionable junction safety intelligence.

---

## 🚀 Live Demo

* 🔗 **Live Web Application**: **[https://junctionguard-ai-jxn1.onrender.com](https://junctionguard-ai-jxn1.onrender.com)**


---

## ✨ 6 Core Feature Pillars

### 1. 🏠 Command Center (3D Digital Twin & Surveillance)
- **Real-Time GIS Radar**: Interactive spatial map with street navigation default and multi-layer tactical rendering.
- **3D Circular Risk Gauge**: Animated SVG telemetry gauge with dynamic severity color gradients (`HIGH`, `MEDIUM`, `LOW`).
- **Primary Driver Breakdown**: Instant view of the dominant risk factor (e.g. *Historical Accident Severity*, *Spatial Conflict*).
- **Monitored Urban Nodes Directory**: Interactive grid with **1-click auto-focus** that smoothly scrolls directly to the live map and telemetry centerpiece.

### 2. 🗺️ Junction Radar & Spatial Hazard Map
- **OpenStreetMap Street View**: Full street geometry, cross-street labels, and landmark annotations.
- **Safety Buffers & Halos**: Configurable proximity circles (250m, 500m, 1000m) and pulsing radar halos around critical hotspots.
- **Accident Density HeatMap**: Gaussian density layers revealing multi-year collision clusters.
- **Multi-City Filtration**: Rapidly isolate nodes across Bengaluru, Mumbai, Delhi, Pune, Kolhapur, Hyderabad, and Chennai.

### 3. 📹 Live CCTV Vision Analytics
- **YOLOv8n Edge Inference**: Real-time detection of cars, motorcycles, buses, trucks, bicycles, and pedestrians.
- **Vulnerable Road User (VRU) Index**: Automatic computation of **Two-Wheeler Share %** and pedestrian conflict density.
- **Interactive Scrubber**: Timeline seek bar to inspect individual frames, confidence bounds, and multi-object tracking IDs.
- **Continuous Live Streaming**: Resilient loop handler and video pipeline with live FPS telemetry.

### 4. 🧠 Explainable AI (XAI) Risk Analysis
- **100% White-Box Formula**: Every junction risk score is mathematically decomposed into 5 weighted components:
  $$\text{Risk Score} = 0.30 \cdot \text{HistoricalAccidents} + 0.20 \cdot \text{TrafficDensity} + 0.20 \cdot \text{NearMisses} + 0.15 \cdot \text{PedestrianActivity} + 0.15 \cdot \text{CitizenHazards}$$
- **Interactive Spider Radar Chart**: Multi-axis factor balance visualization.
- **Historical Baseline**: City and junction crash statistics from verified MoRTH accident records.
- **"What-If" Counterfactual Intervention Sandbox**: Real-time sliders simulating speed calming, surface repairs, and two-wheeler lanes to project quantitative risk reduction ($\Delta$).

### 5. 📊 Fleet Analytics & Macro Intelligence
- **City-by-City Benchmarking**: Plotly horizontal bar ranking showing national risk disparities.
- **National Severity Donut Chart**: Proportional risk profile distribution across surveillance fleet.
- **Two-Wheeler Exposure vs Risk Score**: Scatter analysis highlighting high-risk vulnerable corridors.
- **Corridor Priority Matrix**: Automated triage ranking junctions by immediate intervention urgency.

### 6. 👥 Citizen Hazard Reporting & Cloud Evidence
- **Interactive Map Pin-Drop & Geocoding**: Search bar, GPS one-tap auto-pin, and nearest junction detection.
- **Target Location Dynamic Sync**: Dropped pins automatically select or generate junction records.
- **Cloud Media Uploads**: Full photo/video evidence stored securely in **Supabase Cloud Storage** with local disk backup.
- **Automated Form Reset**: Clean widget reset upon submission and immediate AI risk recalculation.

---

## 🏗️ Technical Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       JUNCTIONGUARD AI PLATFORM                         │
│             Streamlit Modern Full-Width Top Navigation UI               │
└──────────────┬────────────────────┬────────────────────┬────────────────┘
               │                    │                    │
        ┌──────▼──────┐      ┌──────▼──────┐      ┌──────▼──────┐
        │Vision Module│      │ Risk Engine │      │ Citizen     │
        │ YOLOv8n     │      │ 5-Factor    │      │ Reporting   │
        │ ByteTrack   │      │ Weighted    │      │ Portal      │
        └──────┬──────┘      └──────┬──────┘      └──────┬──────┘
               │                    │                    │
        ┌──────▼──────┐      ┌──────▼──────┐      ┌──────▼──────┐
        │Frame Extract│      │MoRTH India  │      │SQLite DB +  │
        │ Telemetry   │      │Accident Data│      │Supabase     │
        └─────────────┘      │ (3,000 rec) │      │Cloud Storage│
                             └─────────────┘      └─────────────┘
```

### Tech Stack

| Layer | Technology |
|---|---|
| **Frontend UI** | Streamlit ≥ 1.30, Custom Quantum Glassmorphism CSS |
| **Mapping & GIS** | Folium ≥ 0.15, streamlit-folium, OpenStreetMap + Esri |
| **Computer Vision** | YOLOv8n (Ultralytics ≥ 8.1), OpenCV-headless ≥ 4.8 |
| **Data Processing** | Pandas ≥ 2.0, NumPy ≥ 1.24 |
| **Visualization** | Plotly ≥ 5.18 |
| **Primary Database** | SQLite (`junctions.db`) |
| **Cloud Storage & Sync** | Supabase (PostgreSQL + `citizen-reports` Storage Bucket) |
| **Geocoding** | OpenStreetMap Nominatim API, Reverse Haversine Geocoder |
| **Stream Ingestion** | yt-dlp ≥ 2024.1 |
| **Deployment** | Render Web Service (`render.yaml`), UptimeRobot Keep-Alive |

---

## 📦 Setup & Installation

### Prerequisites
- Python 3.10 or 3.11
- Git
- (Optional) Supabase credentials for cloud sync

### 1. Clone the Repository
```bash
git clone https://github.com/shubhodbirajdar928-hash/JUNCTIONGUARD--AI.git
cd JUNCTIONGUARD--AI
```

### 2. Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate        # On macOS/Linux
# venv\Scripts\activate         # On Windows
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-key
```

### 5. Run the Application
```bash
streamlit run app.py
```
Open **`http://localhost:8501`** in your browser.

---
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

> ℹ️ If Supabase credentials are not provided, the app automatically falls back to the local SQLite database.

### 5. Run the Application

```bash
streamlit run app.py
```

The app will open at **`http://localhost:8501`**

### 6. (Optional) Process a Video File

```python
from src.vision.video_processor import VideoTrafficDetector

detector = VideoTrafficDetector()
result = detector.process_video("data/sample_videos/junction.mp4", output_dir="data/output")
print(result)
```

---

## 📁 Project Structure

```
JunctionGuard-AI/
├── app.py                          # Main Streamlit dashboard (1,408 lines)
├── app/
│   ├── components.py               # Reusable UI components & custom styles
│   ├── pages/
│   │   └── 1_Citizen_Report.py     # Citizen hazard reporting portal
│   └── data_loader.py              # App-level data utilities
├── src/
│   ├── analytics/
│   │   ├── risk_engine.py          # Explainable 5-factor risk scoring
│   │   ├── data_loader.py          # Kaggle accident dataset pipeline
│   │   └── indicator_engine.py     # Traffic indicator computation
│   ├── vision/
│   │   ├── detector.py             # YOLOv8 + OpenCV detection engine
│   │   ├── video_processor.py      # Frame extraction & JSON export
│   │   ├── stream_processor.py     # Live CCTV stream handling
│   │   └── analyzer.py             # Vision analytics aggregator
│   ├── database.py                 # SQLite CRUD + schema + seed data
│   ├── supabase_client.py          # Cloud real-time sync
│   ├── geo_utils.py                # Haversine, geocoding, IP location
│   └── schema.py                   # Pydantic data models
├── data/
│   ├── india_road_accidents_3000.csv   # Kaggle accident dataset
│   ├── citizen_reports/                # Crowdsourced report storage
│   ├── sample_videos/                  # Sample CCTV footage
│   └── output/                         # Detection JSON/CSV exports
├── tests/                          # Unit tests
├── scripts/                        # Utility scripts
├── yolov8n.pt                      # YOLOv8 nano model weights
├── junctions.db                    # SQLite database
├── render.yaml                     # Render deployment config
├── requirements.txt                # Python dependencies
├── .streamlit/                     # Streamlit configuration
├── README.md
├── LICENSE
├── SECURITY.md
├── CONTRIBUTING.md
└── CODE_OF_CONDUCT.md
```

---

## 🗺️ Monitored Junctions

| Junction | City | State | Risk Level |
|---|---|---|---|
| Silk Board Junction | Bengaluru | Karnataka | 🔴 HIGH (88.4) |
| Goraguntepalya Junction | Bengaluru | Karnataka | 🔴 HIGH (82.1) |
| ITO Crossing | New Delhi | Delhi | 🔴 HIGH (76.2) |
| Panjagutta Junction | Hyderabad | Telangana | 🟡 MEDIUM (64.8) |
| Dadar TT Circle | Mumbai | Maharashtra | 🟡 MEDIUM (58.5) |
| Kathipara Junction | Chennai | Tamil Nadu | 🟡 MEDIUM (42.0) |
| Dabholkar Corner | Kolhapur | Maharashtra | 🟡 MEDIUM (40.8) |
| Shivaji Chowk | Kolhapur | Maharashtra | 🟢 LOW (38.0) |
| Rajaram Corner | Kolhapur | Maharashtra | 🟢 LOW (36.0) |
| Cyber Chowk | Kolhapur | Maharashtra | 🟢 LOW (34.0) |
| Chandani Chowk Junction | Pune | Maharashtra | 🟢 LOW (31.5) |
| Kawala Naka | Kolhapur | Maharashtra | 🟢 LOW |

---

## 👥 Team & Contributions

| Name | Role | Contributions |
|---|---|---|
| **Shubhod** | Team Lead / Full-Stack Developer | System architecture, main dashboard (`app.py`), database design, deployment on Render |
| **Saiprasad** | Computer Vision & Analytics Engineer | YOLOv8 integration, `src/vision/` pipeline, XAI risk engine (`risk_engine.py`), dataset pipelines |
| **Shubhod & Saiprasad** | Frontend / UI & Product Design | Quantum Glassmorphism interface, Folium GIS map integration, custom animations, test suite |
| **Shubhod** | Backend & DevOps | Supabase integration, geo-utilities, citizen reporting portal, Render CI/CD |



---

## 🚀 Deployment

### Render (Cloud)

The project includes a `render.yaml` configuration for one-click Render deployment:

```bash
# Push to your repository — Render auto-deploys on push
git push origin main
```

### Local Docker (Optional)

```bash
docker build -t junctionguard-ai .
docker run -p 8501:8501 junctionguard-ai
```

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

```bash
# Test Supabase connectivity specifically
python test_supabase_connection.py
```

---

## 📊 Risk Scoring Formula

```
Risk Score (0–100) =
    (Historical Accident Score × 0.30)
  + (Traffic Density Score    × 0.20)
  + (Near-Miss Conflict Score × 0.20)
  + (Pedestrian Activity Score× 0.15)
  + (Citizen Reports Score    × 0.15)
```

All component scores are normalized to a 0–100 scale before weighting.

---

## 🔮 Future Roadmap

- [ ] Real CCTV RTSP/HLS stream integration with municipal feeds
- [ ] WebSocket live dashboard push updates
- [ ] Mobile PWA for citizen reporting
- [ ] SMS/WhatsApp alert system for traffic police
- [ ] Custom YOLOv8 fine-tuning on Indian traffic scenes (auto-rickshaws, cycle-rickshaws)
- [ ] LSTM/Prophet predictive risk forecasting
- [ ] Government PDF/Excel reporting portal
- [ ] Pan-India expansion (500+ junctions, 50 cities)
- [ ] NHAI & MoRTH integration

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](./LICENSE) file for details.

---

## 🔒 Security

See [SECURITY.md](./SECURITY.md) for information on how data is handled, stored, and protected.

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines on how to get started.

---

## 📬 Contact

For queries related to this project, please open an issue on GitHub or reach out via the hackathon submission portal.

---

<div align="center">

**Built with ❤️ for OMNIKON Hackathon**

*JunctionGuard AI — Roads Safer, Cities Smarter.*

</div>
