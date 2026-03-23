from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
import uvicorn

from weather import get_weather
from flood_risk import calculate_flood_risk
from ai_advisory import get_marathi_advisory
from village_data import load_villages, get_village

# ── App setup ──────────────────────────────────────────────────────────────────
app = FastAPI(
    title="KonkanRakshak API",
    description=(
        "🌊 AI-Powered Flood Alert & Crop Advisory System for Sindhudurg district, Maharashtra.\n\n"
        "Built by Sumit (Sawantwadi) — Mechanical → Cloud/AI Engineer.\n\n"
        "**Stack:** Python · FastAPI · Groq AI · OpenWeatherMap · Docker · GitHub Actions"
    ),
    version="1.0.0",
    contact={
        "name": "Sumit — Sawantwadi, Sindhudurg",
        "url": "https://github.com/your-username/konkan-rakshak",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load village data once at startup
villages_df = load_villages()


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.get("/", tags=["Info"])
async def root():
    """Project info and available endpoints."""
    return {
        "project": "KonkanRakshak 🌊",
        "description": "AI-Powered Flood Alert & Crop Advisory — Sindhudurg, Maharashtra",
        "status": "live",
        "villages_loaded": len(villages_df),
        "endpoints": {
            "list_villages":  "GET /villages",
            "flood_alert":    "GET /flood-alert/{village_name}",
            "api_docs":       "GET /docs",
            "health":         "GET /health",
        },
        "built_by": "Sumit — Sawantwadi, Sindhudurg",
    }


@app.get("/health", tags=["Info"])
async def health():
    """Health check — used by CI/CD pipeline and Render.com."""
    return {
        "status": "healthy",
        "villages_loaded": len(villages_df),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/villages", tags=["Villages"])
async def list_villages():
    """List all available villages."""
    return {
        "count": len(villages_df),
        "villages": villages_df["village_name"].tolist(),
        "district": "Sindhudurg, Maharashtra",
    }


@app.get("/flood-alert/{village_name}", tags=["Alerts"])
async def flood_alert(village_name: str):
    """
    Get real-time flood risk + Marathi crop advisory for a village.

    - **village_name**: e.g. `Malvan`, `Sawantwadi`, `Vengurla`
    - Returns weather data, flood risk score (0–100), and Marathi AI advisory.

    Try: `/flood-alert/Malvan`
    """
    village = get_village(villages_df, village_name)
    if not village:
        all_names = villages_df["village_name"].tolist()
        raise HTTPException(
            status_code=404,
            detail={
                "error": f"Village '{village_name}' not found.",
                "tip": "Check /villages for the full list.",
                "available": all_names,
            },
        )

    weather  = await get_weather(village["lat"], village["lon"])
    risk     = calculate_flood_risk(weather, village)
    advisory = await get_marathi_advisory(
        village["village_name"], village["main_crops"], weather, risk
    )

    return {
        "village":          village["village_name"],
        "taluka":           village["taluka"],
        "district":         "Sindhudurg",
        "weather":          weather,
        "flood_risk":       risk,
        "marathi_advisory": advisory,
        "generated_at":     datetime.now(timezone.utc).isoformat(),
    }


# ── Dev server ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
