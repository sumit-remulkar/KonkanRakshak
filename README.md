# 🌊 KonkanRakshak

**AI-Powered Flood Alert & Crop Advisory System for Sindhudurg District, Maharashtra**

[![CI/CD](https://github.com/YOUR_USERNAME/konkan-rakshak/actions/workflows/deploy.yml/badge.svg)](https://github.com/YOUR_USERNAME/konkan-rakshak/actions)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-ready-blue)](https://docker.com)
[![Live](https://img.shields.io/badge/Live-Render.com-brightgreen)](https://konkan-rakshak.onrender.com)

> Built by **Sumit** from Sawantwadi, Sindhudurg — Mechanical Diploma → Cloud/AI Engineer

---

## 🎯 What It Does

KonkanRakshak helps farmers and local authorities in **Sindhudurg district** by:

- 🌦️ Fetching **real-time weather** (rainfall, humidity, wind) for any village
- 📊 Calculating a **flood risk score (0–100)** calibrated for Konkan's 3000mm+ annual rainfall
- 🤖 Generating **Marathi-language crop advisory** using Groq AI (LLaMA3)
- 📡 Exposing a clean **REST API** accessible from any device

**Live demo:** `https://konkan-rakshak.onrender.com/flood-alert/Malvan`

---

## 🔧 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11 + FastAPI |
| Weather | OpenWeatherMap API (free tier) |
| AI Advisory | Groq API — llama3-8b-8192 (free) |
| Language | Marathi (मराठी) |
| Container | Docker |
| CI/CD | GitHub Actions |
| Deployment | Render.com (free tier) |

---

## 📁 Project Structure

```
konkan-rakshak/
├── app/
│   ├── main.py            # FastAPI entry point
│   ├── weather.py         # OpenWeatherMap integration
│   ├── flood_risk.py      # Flood risk score engine
│   ├── ai_advisory.py     # Groq AI Marathi advisory
│   └── village_data.py    # CSV loader
├── data/
│   └── sindhudurg_villages.csv   # 15 Sindhudurg villages
├── .github/workflows/
│   └── deploy.yml         # GitHub Actions CI/CD
├── Dockerfile
├── requirements.txt
└── .env.example
```

---

## 🚀 Run Locally

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/konkan-rakshak.git
cd konkan-rakshak

# 2. Setup
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt

# 3. Add API keys
cp .env.example .env
# Edit .env — add your OpenWeatherMap + Groq keys

# 4. Run
cd app
uvicorn main:app --reload

# 5. Open
# http://localhost:8000/docs
```

---

## 🐳 Run with Docker

```bash
docker build -t konkan-rakshak .
docker run -p 8000:8000 --env-file .env konkan-rakshak
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Project info |
| GET | `/health` | Health check |
| GET | `/villages` | List all villages |
| GET | `/flood-alert/{village}` | Full alert + Marathi advisory |

**Example response** — `GET /flood-alert/Malvan`:

```json
{
  "village": "Malvan",
  "taluka": "Malvan",
  "weather": {
    "temp_c": 29.2,
    "humidity": 88,
    "rainfall_1h": 12.5,
    "wind_kmh": 22.0
  },
  "flood_risk": {
    "score": 55,
    "level": "MEDIUM",
    "action": "Stay alert. Monitor water levels. Secure crops."
  },
  "marathi_advisory": "१. आजचा पीक सल्ला: ..."
}
```

---

## 🌍 Villages Covered

Malvan · Vengurla · Kudal · Sawantwadi · Kankavli · Vaibhavwadi · Devgad · Sindhudurg · Oros · Banda · Shiroda · Nerur · Phondaghat · Tulas · Lanja

---

## ⚙️ CI/CD Pipeline

Every push to `main` branch:
1. Builds Docker image
2. Runs health check tests
3. Auto-deploys to Render.com

---

## 🔑 Environment Variables

```
OPENWEATHER_API_KEY   # from openweathermap.org (free)
GROQ_API_KEY          # from console.groq.com (free)
```

---

## 📄 License

MIT — free to use and build upon.
