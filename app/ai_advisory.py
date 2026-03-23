import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_KEY = os.getenv("GROQ_API_KEY")


def _mock_advisory(village: str, crops: str, risk_level: str) -> str:
    """Fallback when no real Groq key is set — for local testing."""
    return (
        f"[MOCK — add real GROQ_API_KEY for live Marathi advisory]\n\n"
        f"गाव: {village} | पिके: {crops} | धोका: {risk_level}\n\n"
        "१. आजचा पीक सल्ला: हे mock उत्तर आहे. खरी Groq API key जोडा.\n"
        "२. पूर सतर्कता: GROQ_API_KEY .env मध्ये set करा.\n"
        "३. तातडीचे उपाय: console.groq.com वर free key मिळवा."
    )


async def get_marathi_advisory(
    village: str, crops: str, weather: dict, risk: dict
) -> str:
    if not GROQ_KEY or GROQ_KEY == "your_groq_key":
        return _mock_advisory(village, crops, risk["level"])

    client = Groq(api_key=GROQ_KEY)

    prompt = f"""तुम्ही सिंधुदुर्ग जिल्ह्यातील एक अनुभवी कृषी तज्ञ आहात.
कृपया केवळ शुद्ध मराठीत उत्तर द्या, इंग्रजी वापरू नका.

गाव: {village}
मुख्य पिके: {crops}
सध्याचे तापमान: {weather['temp_c']}°C
आर्द्रता: {weather['humidity']}%
पाऊस: {weather['rainfall_1h']} mm/तास
वारा: {weather['wind_kmh']} km/h
पूर धोका पातळी: {risk['level']} (गुण: {risk['score']}/100)

खालील तीन मुद्द्यांवर सल्ला द्या:
१. आजचा पीक सल्ला (२-३ वाक्ये)
२. पूर सतर्कता व खबरदारी (लागू असल्यास)
३. शेतकऱ्यांसाठी तातडीचे व्यावहारिक उपाय

सल्ला साधा, स्पष्ट आणि व्यावहारिक असावा."""

    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.7,
    )
    return resp.choices[0].message.content
