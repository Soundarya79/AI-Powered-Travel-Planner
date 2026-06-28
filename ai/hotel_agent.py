import json
import time
from google import genai

from config import GEMINI_API_KEY
from ai.prompt_builder import load_prompt

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_hotels(data):

    prompt = load_prompt("hotel_prompt.txt")

    prompt = prompt.replace("{destination}", data["destination"])
    prompt = prompt.replace("{budget}", str(data["budget"]))
    prompt = prompt.replace("{experience}", data["experience"])
    prompt = prompt.replace("{trip_type}", data["trip_type"])

    response = None

    for _ in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt
            )
            break
        except Exception:
            time.sleep(5)

    if response is None:
        raise Exception("Failed to get response from Gemini.")

    text = response.text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)