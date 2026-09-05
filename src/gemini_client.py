from google import genai
from dotenv import load_dotenv
import os


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(
    api_key=api_key
)


def generate_content(prompt):

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        error_message = str(e)

        if "503" in error_message or "UNAVAILABLE" in error_message:

            return (
                "⚠️ Gemini is temporarily unavailable because "
                "the model is experiencing high demand. "
                "Please try again in a moment."
            )

        return (
            f"⚠️ Gemini request failed: {error_message}"
        )