import httpx
import os
from dotenv import load_dotenv

load_dotenv()

OWM_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


async def get_weather(lat: float, lon: float) -> dict:
    if not OWM_KEY or OWM_KEY == "your_openweathermap_key":
        # Return mock data for testing without a real key
        return {
            "temp_c": 28.5,
            "humidity": 82,
            "rainfall_1h": 5.2,
            "wind_kmh": 18.0,
            "description": "moderate rain",
            "clouds_pct": 75,
            "mock": True,
        }

    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(
            BASE_URL,
            params={
                "lat": lat,
                "lon": lon,
                "appid": OWM_KEY,
                "units": "metric",
            },
        )
        r.raise_for_status()
        d = r.json()

        return {
            "temp_c": d["main"]["temp"],
            "humidity": d["main"]["humidity"],
            "rainfall_1h": d.get("rain", {}).get("1h", 0.0),
            "wind_kmh": round(d["wind"]["speed"] * 3.6, 1),
            "description": d["weather"][0]["description"],
            "clouds_pct": d["clouds"]["all"],
            "mock": False,
        }
