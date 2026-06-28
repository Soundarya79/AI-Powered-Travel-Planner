import json

from google import genai

from config import GEMINI_API_KEY
from ai.prompt_builder import build_itinerary_prompt

client = genai.Client(api_key=GEMINI_API_KEY)


def clean_json(text):

    text = text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "")

    if text.endswith("```"):
        text = text.replace("```", "")

    return text.strip()


def validate_response(data):

    defaults = {
        "destination": "",
        "trip_theme": "",
        "best_time_to_visit": "",
        "hotels": [],
        "recommendation": {},
        "days": [],
        "meals": {
            "breakfast": [],
            "lunch": [],
            "dinner": [],
        },
        "popular_foods": [],
        "popular_places": [],
    }

    for key, value in defaults.items():
        if key not in data:
            data[key] = value

    return data


def generate_itinerary(data):

    prompt = build_itinerary_prompt(data)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = clean_json(response.text)

    try:

        itinerary = json.loads(text)

    except json.JSONDecodeError:

        print(text)

        raise Exception("Gemini returned invalid JSON.")

    itinerary = validate_response(itinerary)

    return itinerary
