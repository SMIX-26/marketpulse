import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY is not set in .env")

client = genai.Client(
    api_key=api_key
)


def generate_ai_explanation(
    symbol: str,
    price_change_percent: float,
    volume_ratio: float,
    news_count: int,
    attention_level: str,
):

    prompt = f"""
You are a financial market explanation assistant for MarketPulse.

Analyze this stock activity:

Stock: {symbol}
Price change since last visit: {price_change_percent:.2f}%
Trading volume compared with normal: {volume_ratio:.2f}x
New news events: {news_count}
Attention level: {attention_level}

Generate a concise explanation in 1-2 sentences.

Rules:
- Explain the data in simple language.
- Do not give investment advice.
- Do not say buy, sell, or hold.
- Do not invent news or events.
- Only use the information provided.
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        if response.text:
            return response.text.strip()

        return "No AI explanation was generated."

    except Exception as e:

        print("Gemini API Error:", repr(e))

        return (
            f"AI explanation unavailable. "
            f"Price changed {price_change_percent:.2f}% "
            f"with {volume_ratio:.2f}x normal trading volume."
        )