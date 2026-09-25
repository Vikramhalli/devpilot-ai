import time

from google import genai

from app.core.config import settings


client = genai.Client(
    api_key=settings.google_api_key
)


MODELS = [
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.6-flash",
]


def analyze_code(code: str) -> str:
    prompt = f"""
You are an expert software engineer reviewing source code.

Analyze the following code and provide:

1. Explanation
2. Potential Bugs or Issues
3. Suggestions for Improvement

Be specific and practical.

Code:

{code}
"""

    last_error = None

    for model in MODELS:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                )

                if response.text:
                    return response.text

                raise RuntimeError(
                    "AI returned an empty response."
                )

            except Exception as error:
                last_error = error

                error_code = getattr(error, "code", None)

                print(
                    f"AI model {model} failed "
                    f"(attempt {attempt + 1}/3): {error}"
                )

                # Quota exhausted:
                # immediately move to the fallback model.
                if error_code == 429:
                    break

                # Temporary server overload:
                # retry with exponential backoff.
                if error_code == 503 and attempt < 2:
                    delay = 2 ** attempt

                    print(
                        f"Retrying {model} in {delay} seconds..."
                    )

                    time.sleep(delay)
                    continue

                # Other errors:
                # move to the next model.
                break

        print(
            f"Model {model} unavailable. "
            "Trying fallback model."
        )

    raise RuntimeError(
        "AI analysis is temporarily unavailable. "
        "All configured Gemini models are currently unavailable."
    ) from last_error