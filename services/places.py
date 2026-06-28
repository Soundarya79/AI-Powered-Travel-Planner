import requests
from services.geocoder import get_coordinates
def get_places(city, category="tourism", limit=10):

    coords = get_coordinates(city)

    if not coords:
        return []

    lat = coords["lat"]
    lon = coords["lon"]

    query = f"""
    [out:json];
    (
      node["{category}"](around:15000,{lat},{lon});
      way["{category}"](around:15000,{lat},{lon});
      relation["{category}"](around:15000,{lat},{lon});
    );
    out center;
    """

    url = "https://overpass-api.de/api/interpreter"

    response = requests.post(
        url,
        data=query,
        headers={"User-Agent": "VoyageAI/1.0"},
        timeout=30
    )

    data = response.json()

    results = []

    for item in data.get("elements", [])[:limit]:

        tags = item.get("tags", {})

        results.append({
            "name": tags.get("name", "Unknown"),
            "type": list(tags.values())[0] if tags else "Unknown"
        })

    return results