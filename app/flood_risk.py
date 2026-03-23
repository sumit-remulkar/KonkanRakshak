def calculate_flood_risk(weather: dict, village: dict) -> dict:
    """
    Flood risk score 0–100.
    Calibrated for Konkan region — Sindhudurg gets 3000mm+ rain annually.

    Factors:
      - Rainfall intensity (50 pts max)
      - Humidity         (20 pts max)
      - Village elevation (20 pts max)
      - Historical flood zone from CSV (10 pts max)
    """
    score = 0

    # --- Rainfall intensity (max 50 pts) ---
    rain = weather.get("rainfall_1h", 0)
    if rain >= 50:
        score += 50
    elif rain >= 20:
        score += 30
    elif rain >= 10:
        score += 15
    elif rain >= 5:
        score += 8
    elif rain >= 2:
        score += 3

    # --- Humidity (max 20 pts) ---
    humidity = weather.get("humidity", 0)
    if humidity >= 90:
        score += 20
    elif humidity >= 80:
        score += 12
    elif humidity >= 70:
        score += 6

    # --- Elevation — lower = higher flood risk (max 20 pts) ---
    elevation = village.get("elevation_m", 50)
    if elevation < 10:
        score += 20
    elif elevation < 20:
        score += 15
    elif elevation < 40:
        score += 8
    elif elevation < 60:
        score += 3

    # --- Historical flood zone from CSV (max 10 pts) ---
    if village.get("flood_prone"):
        score += 10

    score = min(score, 100)

    if score >= 70:
        level = "HIGH"
        color = "red"
        action = "Immediate evacuation alert. Contact local authorities."
    elif score >= 40:
        level = "MEDIUM"
        color = "orange"
        action = "Stay alert. Monitor water levels. Secure crops."
    else:
        level = "LOW"
        color = "green"
        action = "Normal conditions. Continue regular farming activities."

    return {
        "score": score,
        "level": level,
        "color": color,
        "action": action,
        "rainfall_mm_per_hr": rain,
    }
