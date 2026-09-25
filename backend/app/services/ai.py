from google import genai

from app.core.config import settings


def analyze_code(code: str) -> str:
    if not settings.google_api_key:
        raise ValueError(
            "GOOGLE_API_KEY is missing from .env"
        )

    client = genai.Client(
        api_key=settings.google_api_key
    )

    prompt = f"""
You are an expert software engineer.

Analyze the following source code.

Provide:
1. A simple explanation of what the code does.
2. Potential bugs or issues.
3. Suggestions for improvement.

Keep the response practical and concise.

Source code:

{code}
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt,
    )

    return response.text or "No analysis returned."