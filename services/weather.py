import requests

from services.geocoder import get_coordinates


def get_weather(city):

    location = get_coordinates(city)

    if not location:
        return None

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": location["lat"],
        "longitude": location["lon"],
        "current": [
            "temperature_2m",
            "weather_code",
            "wind_speed_10m"
        ]
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        data = response.json()

        current = data["current"]

        code = current["weather_code"]

        weather = {
            0: "Clear Sky",
            1: "Mainly Clear",
            2: "Partly Cloudy",
            3: "Cloudy",
            45: "Fog",
            48: "Fog",
            51: "Light Drizzle",
            53: "Drizzle",
            55: "Heavy Drizzle",
            61: "Light Rain",
            63: "Rain",
            65: "Heavy Rain",
            71: "Snow",
            80: "Rain Showers",
            95: "Thunderstorm",
        }

        return {
            "temperature": current["temperature_2m"],
            "condition": weather.get(code, "Unknown"),
            "wind": current["wind_speed_10m"]
        }

    except Exception:

        return None