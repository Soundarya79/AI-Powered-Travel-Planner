import requests
from config import PEXELS_API_KEY


def get_image(query):

    url = "https://api.pexels.com/v1/search"

    headers = {
        "Authorization": PEXELS_API_KEY
    }

    params = {
        "query": query,
        "per_page": 1,
        "orientation": "landscape"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10
        )

        if response.status_code != 200:
            print(response.text)
            return None

        data = response.json()

        if data["photos"]:
            return data["photos"][0]["src"]["large2x"]

    except Exception as e:
        print(e)

    return None