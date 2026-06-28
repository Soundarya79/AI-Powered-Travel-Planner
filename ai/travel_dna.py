import json
from google import genai

from config import GEMINI_API_KEY
from ai.prompt_builder import build_travel_dna_prompt

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_travel_dna(data):

    prompt = build_travel_dna_prompt(data)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)