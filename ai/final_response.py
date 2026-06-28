from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_final_response(travel_dna, hotels, itinerary):

    prompt = f"""
Travel DNA

{travel_dna}

Hotels

{hotels}

Itinerary

{itinerary}

Create one complete travel plan.
Return only JSON.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text