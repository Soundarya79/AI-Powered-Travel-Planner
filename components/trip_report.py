from html import escape
from urllib.parse import quote

import requests
import streamlit as st

from config import (
    GOOGLE_PLACES_API_KEY,
    OPENTRIPMAP_API_KEY,
    PEXELS_API_KEY,
)


FALLBACK_IMAGE = (
    "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2"
    "?auto=format&fit=crop&w=1200&q=80"
)

RESULT_CSS = """
<style>
.trip-result-page {
    max-width: 1100px;
    margin: 28px auto 0;
    padding: 20px;
    border-radius: 18px;
    background: #f7f8fa;
    color: #1a2b4c;
    font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

.trip-result-page * {
    box-sizing: border-box;
    letter-spacing: 0;
}

.trip-result-page a {
    color: #1a73e8 !important;
    font-size: 13px;
    font-weight: 700;
    text-decoration: none !important;
}

.trip-result-page a:hover {
    text-decoration: underline !important;
}

.trip-card {
    border: 1px solid #e8e8ec;
    border-radius: 12px;
    background: #ffffff;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.trip-header {
    display: flex;
    justify-content: space-between;
    gap: 18px;
    align-items: flex-start;
    margin-bottom: 24px;
}

.trip-header-main {
    display: flex;
    gap: 14px;
    align-items: flex-start;
}

.trip-header-icon {
    font-size: 34px;
    line-height: 1;
}

.trip-header h1 {
    margin: 0;
    color: #101f3f;
    font-size: clamp(28px, 4vw, 42px);
    font-weight: 850;
    line-height: 1.05;
}

.trip-header p,
.trip-subtext {
    margin: 7px 0 0;
    color: #6b7280;
    font-size: 15px;
    font-weight: 600;
}

.trip-best-time {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    min-width: max-content;
    padding: 11px 14px;
    border: 1px solid #bbebcd;
    border-radius: 10px;
    background: #ffffff;
    color: #16743b;
    font-size: 14px;
    font-weight: 800;
}

.trip-section {
    margin-bottom: 24px;
    padding: 18px;
}

.trip-section-title {
    display: flex;
    gap: 12px;
    align-items: center;
}

.trip-section-title span {
    color: #1a73e8;
    font-size: 25px;
}

.trip-section-title h2 {
    margin: 0;
    color: #1a2b4c;
    font-size: 20px;
    font-weight: 850;
}

.trip-hotels-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 16px;
    margin-top: 18px;
}

.trip-hotel {
    position: relative;
    overflow: hidden;
    border: 1px solid #e8e8ec;
    border-radius: 12px;
    background: #ffffff;
}

.trip-hotel-image-wrap {
    position: relative;
}

.trip-hotel img,
.trip-activity img,
.trip-restaurant img,
.trip-popular-card img {
    display: block;
    width: 100%;
    object-fit: cover;
}

.trip-hotel img {
    aspect-ratio: 16 / 9;
}

.trip-best-pick {
    position: absolute;
    top: 10px;
    left: 10px;
    padding: 7px 10px;
    border-radius: 8px;
    background: #16813c;
    color: #ffffff;
    font-size: 12px;
    font-weight: 850;
}

.trip-hotel-body {
    padding: 13px;
}

.trip-hotel h3,
.trip-restaurant h4 {
    margin: 0 0 9px;
    color: #17213a;
    font-size: 16px;
    font-weight: 850;
}

.trip-rating {
    margin: 5px 0;
    color: #1f2937;
    font-size: 13px;
    font-weight: 750;
}

.trip-rating .star {
    color: #f59e0b;
}

.trip-rating .reviews {
    color: #6b7280;
    font-weight: 600;
}

.trip-location {
    margin: 8px 0;
    color: #374151;
    font-size: 13px;
    font-weight: 650;
}

.trip-price {
    margin: 9px 0;
    color: #1a7f37;
    font-size: 15px;
    font-weight: 850;
}

.trip-recommendation {
    display: flex;
    gap: 13px;
    align-items: center;
    margin-top: 16px;
    padding: 14px;
    border: 1px solid #c8eed5;
    border-radius: 12px;
    background: #eafaf0;
}

.trip-recommendation-icon {
    color: #1a7f37;
    font-size: 29px;
}

.trip-recommendation strong {
    color: #1a7f37;
    font-weight: 850;
}

.trip-recommendation p {
    margin: 4px 0 0;
    color: #1f2937;
    font-size: 14px;
    font-weight: 600;
}

.trip-main-grid {
    display: grid;
    grid-template-columns: minmax(0, 65%) minmax(0, 35%);
    gap: 20px;
    align-items: start;
    margin-bottom: 24px;
}

.trip-day {
    margin-bottom: 20px;
    overflow: hidden;
}

.trip-day:last-child {
    margin-bottom: 0;
}

.trip-day-header {
    display: flex;
    gap: 11px;
    align-items: center;
    padding: 16px 18px;
    border-bottom: 1px solid #f0ddc1;
    background: #fff7ed;
}

.trip-day-header h3 {
    margin: 0;
    color: #191f32;
    font-size: 18px;
    font-weight: 850;
}

.trip-activity {
    padding: 18px;
    border-bottom: 1px solid #f0f0f2;
}

.trip-activity:last-child {
    border-bottom: 0;
}

.trip-activity-title {
    margin: 0 0 13px;
    color: #1a73e8;
    font-size: 16px;
    font-weight: 850;
}

.trip-activity-body {
    display: grid;
    grid-template-columns: 190px minmax(0, 1fr);
    gap: 16px;
    align-items: start;
}

.trip-activity img {
    aspect-ratio: 1.6 / 1;
    border-radius: 9px;
}

.trip-activity p,
.trip-restaurant p {
    margin: 0 0 9px;
    color: #1f2937;
    font-size: 14px;
    line-height: 1.58;
}

.trip-activity .recommended {
    font-weight: 850;
}

.trip-dining {
    padding: 18px;
}

.trip-dining-header {
    display: flex;
    gap: 11px;
    align-items: flex-start;
    margin-bottom: 18px;
}

.trip-dining-header span {
    color: #16813c;
    font-size: 26px;
}

.trip-dining-header h3 {
    margin: 0;
    color: #16813c;
    font-size: 19px;
    font-weight: 850;
}

.trip-meal {
    margin-bottom: 16px;
    padding: 14px;
    border: 1px solid #e8e8ec;
    border-radius: 12px;
}

.trip-meal-label {
    margin: 0 0 12px;
    font-size: 15px;
    font-weight: 850;
}

.trip-meal-breakfast .trip-meal-label,
.trip-meal-lunch .trip-meal-label {
    color: #f97316;
}

.trip-meal-dinner .trip-meal-label {
    color: #6d3bc4;
}

.trip-restaurant {
    display: grid;
    grid-template-columns: 118px minmax(0, 1fr);
    gap: 12px;
    padding-bottom: 14px;
    margin-bottom: 14px;
    border-bottom: 1px solid #eef0f4;
}

.trip-restaurant:last-child {
    padding-bottom: 0;
    margin-bottom: 0;
    border-bottom: 0;
}

.trip-restaurant img {
    aspect-ratio: 1 / 1;
    border-radius: 9px;
}

.trip-restaurant h4 {
    font-size: 14px;
    margin-bottom: 5px;
}

.trip-restaurant p {
    margin-bottom: 5px;
    font-size: 12.5px;
}

.trip-more-restaurants {
    display: block;
    text-align: center;
    padding-top: 4px;
}

.trip-bottom-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 20px;
    margin-bottom: 24px;
}

.trip-popular-card {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 210px;
    gap: 16px;
    align-items: center;
    padding: 18px;
}

.trip-popular-card h3 {
    margin: 0 0 12px;
    color: #1a2b4c;
    font-size: 17px;
    font-weight: 850;
}

.trip-popular-card ul {
    margin: 0;
    padding-left: 20px;
}

.trip-popular-card li {
    margin: 7px 0;
    color: #374151;
    font-size: 14px;
    font-weight: 650;
}

.trip-place-list li {
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto;
    gap: 8px;
}

.trip-popular-card img {
    aspect-ratio: 1.55 / 1;
    border-radius: 10px;
}

.trip-tip {
    padding: 14px 18px;
    border: 1px solid #d8f1c8;
    border-radius: 12px;
    background: #f0fdf4;
    color: #16743b;
    text-align: center;
    font-size: 15px;
    font-weight: 750;
}

@media (max-width: 900px) {
    .trip-hotels-grid,
    .trip-main-grid,
    .trip-bottom-grid {
        grid-template-columns: 1fr;
    }

    .trip-header {
        display: grid;
    }

    .trip-best-time {
        width: fit-content;
    }
}

@media (max-width: 640px) {
    .trip-result-page {
        padding: 14px;
    }

    .trip-activity-body,
    .trip-restaurant,
    .trip-popular-card,
    .trip-place-list li {
        grid-template-columns: 1fr;
    }

    .trip-activity img,
    .trip-restaurant img,
    .trip-popular-card img {
        max-height: 220px;
    }
}
</style>
"""


def _text(value, fallback=""):
    if value is None:
        return fallback
    if isinstance(value, (list, tuple)):
        return ", ".join(str(item) for item in value if item)
    return str(value)


def _html(value, fallback=""):
    return escape(_text(value, fallback))


def _url(value):
    return escape(_text(value), quote=True)


def _maps_url(query):
    return "https://www.google.com/maps/search/?api=1&query=" + quote(_text(query))


def _booking_url(query):
    return "https://www.booking.com/searchresults.html?ss=" + quote(_text(query))


def _money(value):
    text = _text(value)
    if not text:
        return "Price on request"
    if text.startswith("Rs") or text.startswith("₹") or "per" in text or "/ night" in text:
        return text.replace("₹", "&#8377;").replace("Rs", "&#8377;")
    try:
        return f"&#8377;{int(float(text)):,}"
    except ValueError:
        return text.replace("₹", "&#8377;")


def _cache():
    if "trip_result_image_cache" not in st.session_state:
        st.session_state.trip_result_image_cache = {}
    return st.session_state.trip_result_image_cache


def _request_json(url, **kwargs):
    response = requests.get(url, timeout=8, **kwargs)
    if response.status_code != 200:
        return {}
    return response.json()


def _wikipedia_image(name):
    if not name:
        return None
    url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + quote(name)
    data = _request_json(url)
    return (
        data.get("originalimage", {}).get("source")
        or data.get("thumbnail", {}).get("source")
    )


def _opentripmap_image(name):
    if not name or not OPENTRIPMAP_API_KEY:
        return None
    geoname = _request_json(
        "https://api.opentripmap.com/0.1/en/places/geoname",
        params={"name": name, "apikey": OPENTRIPMAP_API_KEY},
    )
    xid = geoname.get("xid")
    if not xid:
        return None
    place = _request_json(
        f"https://api.opentripmap.com/0.1/en/places/xid/{xid}",
        params={"apikey": OPENTRIPMAP_API_KEY},
    )
    return place.get("preview", {}).get("source") or place.get("image")


def _pexels_image(query):
    if not query or not PEXELS_API_KEY:
        return None
    data = _request_json(
        "https://api.pexels.com/v1/search",
        headers={"Authorization": PEXELS_API_KEY},
        params={"query": query, "per_page": 1, "orientation": "landscape"},
    )
    photos = data.get("photos") or []
    if not photos:
        return None
    return photos[0].get("src", {}).get("large2x") or photos[0].get("src", {}).get("large")


def _google_place_photo(name, location):
    if not name or not GOOGLE_PLACES_API_KEY:
        return None

    search = _request_json(
        "https://maps.googleapis.com/maps/api/place/findplacefromtext/json",
        params={
            "input": f"{name} {location}".strip(),
            "inputtype": "textquery",
            "fields": "photos,place_id",
            "key": GOOGLE_PLACES_API_KEY,
        },
    )
    candidates = search.get("candidates") or []
    photos = candidates[0].get("photos") if candidates else None
    if not photos:
        return None

    reference = photos[0].get("photo_reference")
    if not reference:
        return None
    return (
        "https://maps.googleapis.com/maps/api/place/photo?"
        + quote(f"maxwidth=900&photo_reference={reference}&key={GOOGLE_PLACES_API_KEY}", safe="=&")
    )


def get_image(entity_type, name, location="", destination=""):
    """Route image lookups by content type and cache every result.

    Hotels and restaurants use Google Places photos when GOOGLE_PLACES_API_KEY is
    present. Without that key, they intentionally fall back to representative
    category stock searches because free stock APIs cannot verify exact venues.
    """
    key = "|".join([entity_type, _text(name), _text(location), _text(destination)]).lower()
    image_cache = _cache()
    if key in image_cache:
        return image_cache[key]

    image = None
    clean_name = _text(name)
    clean_location = _text(location) or _text(destination)

    try:
        if entity_type == "attraction":
            image = (
                _wikipedia_image(clean_name)
                or _opentripmap_image(clean_name)
                or _pexels_image(f"{clean_name} {clean_location} landmark travel")
            )
        elif entity_type == "food":
            image = _pexels_image(f"{clean_name} food photography close up")
        elif entity_type == "hotel":
            image = _google_place_photo(clean_name, clean_location) or _pexels_image(
                f"beachfront resort pool {clean_location}"
            )
        elif entity_type == "restaurant":
            image = _google_place_photo(clean_name, clean_location) or _pexels_image(
                f"{clean_location} restaurant food photography"
            )
        else:
            image = _pexels_image(f"{clean_name} {clean_location} travel")
    except Exception:
        image = None

    image_cache[key] = image or FALLBACK_IMAGE
    return image_cache[key]


def _reviews(value):
    text = _text(value)
    if not text:
        return "recent reviews"
    try:
        return f"{int(float(text)):,} reviews"
    except ValueError:
        return text.replace("(", "").replace(")", "")


def _rating(value, fallback="4.5"):
    text = _text(value, fallback)
    if "/" in text:
        return text.split("/")[0].strip()
    if "(" in text:
        return text.split("(")[0].strip()
    return text


def _normalise_hotel(hotel, index):
    return {
        "name": hotel.get("name", "Hotel"),
        "rating": _rating(hotel.get("rating", "4.5")),
        "review_count": hotel.get("review_count") or "verified reviews",
        "location": hotel.get("location", ""),
        "price_per_night": hotel.get("price_per_night", ""),
        "is_best_pick": hotel.get("is_best_pick", index == 0),
        "booking_search_query": (
            hotel.get("booking_search_query")
            or hotel.get("booking_search")
            or hotel.get("name", "")
        ),
        "reason": hotel.get("reason") or hotel.get("why", ""),
    }


def _normalise_block(time_of_day, slot, destination):
    if not isinstance(slot, dict):
        return None
    if "title" in slot:
        return slot

    place = slot.get("place", slot)
    if not isinstance(place, dict) or not place:
        return None

    name = place.get("name") or place.get("place") or f"{time_of_day} in {destination}"
    return {
        "time_of_day": time_of_day,
        "title": name,
        "description": (
            place.get("description")
            or place.get("about")
            or place.get("why_visit")
            or place.get("reason")
            or ""
        ),
        "recommended": place.get("recommended"),
        "location": place.get("location") or name,
        "maps_query": place.get("maps_query") or place.get("google_maps_search") or name,
    }


def _normalise_restaurant(item):
    return {
        "name": item.get("name") or item.get("restaurant") or "Restaurant",
        "rating": _rating(item.get("rating", "4.5")),
        "review_count": item.get("review_count") or "recent reviews",
        "location": item.get("location") or item.get("cuisine") or "",
        "description": item.get("description") or item.get("must_try") or item.get("food") or "",
        "price_range": item.get("price_range") or item.get("cost_for_two") or item.get("cost") or "Cost varies",
        "maps_query": item.get("maps_query") or item.get("google_maps_search") or item.get("name", ""),
        "cuisine": item.get("cuisine", ""),
    }


def _default_trip(trip_data):
    destination = trip_data.get("destination") or "Goa"
    days_count = int(trip_data.get("days") or 4)
    base_days = []
    day_templates = [
        ("Beach Arrival & Sunset Shacks", "Candolim Beach Walk"),
        ("Old Goa, Forts & Local Markets", "Basilica of Bom Jesus"),
        ("South Goa Beaches & Heritage", "Colva Beach"),
        ("Adventure, Markets & North Goa Nightlife", "Kayaking at Nerul River"),
    ]
    for index in range(days_count):
        title, activity = day_templates[index % len(day_templates)]
        base_days.append(
            {
                "day_number": index + 1,
                "day_title": title,
                "blocks": [
                    {
                        "time_of_day": "Morning",
                        "title": activity,
                        "description": "Start with a scenic local experience paced for your trip style.",
                        "recommended": activity,
                        "location": f"{activity}, {destination}",
                    },
                    {
                        "time_of_day": "Afternoon",
                        "title": "Beach Shack Lunch & Relaxation",
                        "description": "Relax by the coast, try fresh seafood, and keep the afternoon easy.",
                        "recommended": "Fisherman's Cove",
                        "location": f"Candolim Beach, {destination}",
                    },
                    {
                        "time_of_day": "Evening",
                        "title": "Market Walk & Local Shopping",
                        "description": "Browse local stalls for souvenirs, clothing, snacks, and music.",
                        "recommended": "Arpora Night Market",
                        "location": f"Arpora, {destination}",
                    },
                    {
                        "time_of_day": "Night",
                        "title": "North Goa Nightlife",
                        "description": "End the day around popular nightlife streets and beach clubs.",
                        "recommended": "Tito's Lane",
                        "location": f"Baga, {destination}",
                    },
                ],
            }
        )

    return {
        "destination": destination,
        "trip_theme": "Adventure, Culture & Relaxation",
        "best_time_to_visit": "Nov - Feb",
        "hotels": [
            {
                "name": "Citrus Prime - Candolim",
                "rating": 4.4,
                "review_count": 1100,
                "location": "Candolim Beach, Goa",
                "price_per_night": 3200,
                "is_best_pick": True,
                "booking_search_query": "Citrus Prime Candolim Goa",
            },
            {
                "name": "Bloom Hotel - Calangute",
                "rating": 4.2,
                "review_count": 1250,
                "location": "Calangute Beach, Goa",
                "price_per_night": 2800,
                "booking_search_query": "Bloom Hotel Calangute Goa",
            },
            {
                "name": "De Mandarin Beach Resort - Morjim",
                "rating": 4.6,
                "review_count": 980,
                "location": "Morjim Beach, Goa",
                "price_per_night": 4100,
                "booking_search_query": "De Mandarin Beach Resort Morjim Goa",
            },
        ],
        "recommendation": {
            "hotel_name": "Citrus Prime - Candolim",
            "reason": "Excellent location, great reviews, and within your budget!",
        },
        "days": base_days,
        "meals": {
            "breakfast": [
                {
                    "name": "Infantaria Cafe",
                    "rating": 4.5,
                    "review_count": 2356,
                    "location": "Calangute, Goa",
                    "description": "Popular for hearty breakfast and great coffee.",
                    "price_range": "Rs 300 - Rs 600 per person",
                }
            ],
            "lunch": [
                {
                    "name": "Fisherman's Cove",
                    "rating": 4.6,
                    "review_count": 1842,
                    "location": "Candolim Beach, Goa",
                    "description": "Famous for seafood and beach vibes.",
                    "price_range": "Rs 800 - Rs 1,500 per person",
                },
                {
                    "name": "Souza Lobo",
                    "rating": 4.4,
                    "review_count": 1213,
                    "location": "Calangute, Goa",
                    "description": "Authentic Goan cuisine since 1932.",
                    "price_range": "Rs 700 - Rs 1,200 per person",
                },
            ],
            "dinner": [
                {
                    "name": "Thalassa",
                    "rating": 4.5,
                    "review_count": 1987,
                    "location": "Siolim, North Goa",
                    "description": "Riverside dining with a beautiful ambience.",
                    "price_range": "Rs 1,200 - Rs 2,000 per person",
                }
            ],
        },
        "popular_foods": [
            "Goan Fish Curry & Rice",
            "Prawn Balchao",
            "Chicken Xacuti",
            "Bebinca (Goan Dessert)",
            "Feni (Local Drink)",
        ],
        "popular_places": [
            {"name": "Basilica of Bom Jesus", "maps_query": "Basilica of Bom Jesus Goa"},
            {"name": "Fort Aguada", "maps_query": "Fort Aguada Goa"},
            {"name": "Anjuna Beach", "maps_query": "Anjuna Beach Goa"},
            {"name": "Dudhsagar Falls", "maps_query": "Dudhsagar Falls Goa"},
            {"name": "Chapora Fort", "maps_query": "Chapora Fort Goa"},
        ],
    }


def _normalise_trip(trip_data, raw):
    if raw and raw.get("days"):
        trip = _default_trip(trip_data)
        trip.update(raw)
    else:
        trip = _default_trip(trip_data)
        if raw:
            destination_obj = raw.get("destination", {})
            if not isinstance(destination_obj, dict):
                destination_obj = {}
            destination = (
                raw.get("destination")
                if isinstance(raw.get("destination"), str)
                else destination_obj.get("name")
            ) or trip_data.get("destination") or "Goa"
            hotels_raw = raw.get("hotels", [])
            if isinstance(hotels_raw, dict):
                hotels_raw = hotels_raw.get("recommended", [])
            days_raw = []
            for old_day in raw.get("itinerary", []):
                blocks = [
                    block
                    for block in [
                        _normalise_block("Morning", old_day.get("morning"), destination),
                        _normalise_block("Afternoon", old_day.get("afternoon"), destination),
                        _normalise_block("Evening", old_day.get("evening"), destination),
                        _normalise_block("Night", old_day.get("night"), destination),
                    ]
                    if block
                ]
                days_raw.append(
                    {
                        "day_number": old_day.get("day", len(days_raw) + 1),
                        "day_title": old_day.get("theme", "Local Experiences"),
                        "blocks": blocks,
                    }
                )

            meals = raw.get("meals")
            if not meals:
                meals = {"breakfast": [], "lunch": [], "dinner": []}
                for old_day in raw.get("itinerary", [])[:1]:
                    for key, meal_key in [
                        ("morning", "breakfast"),
                        ("afternoon", "lunch"),
                        ("night", "dinner"),
                    ]:
                        restaurant = old_day.get(key, {}).get("restaurant", {})
                        if restaurant:
                            meals[meal_key].append(_normalise_restaurant(restaurant))

            foods = [
                food.get("name", "Local dish") if isinstance(food, dict) else _text(food)
                for food in raw.get("must_try_food", [])
            ]
            places = [
                {
                    "name": place.get("name", "Place"),
                    "maps_query": place.get("google_maps_search") or place.get("maps_query") or place.get("name", ""),
                }
                for place in raw.get("must_visit", [])
                if isinstance(place, dict)
            ]

            trip.update(
                {
                    "destination": destination,
                    "trip_theme": raw.get("trip_theme")
                    or raw.get("summary", {}).get("tagline")
                    or trip.get("trip_theme"),
                    "best_time_to_visit": raw.get("best_time_to_visit")
                    or destination_obj.get("best_time")
                    or trip.get("best_time_to_visit"),
                    "hotels": hotels_raw or trip.get("hotels", []),
                    "recommendation": raw.get("recommendation") or trip.get("recommendation", {}),
                    "days": days_raw or trip.get("days", []),
                    "meals": meals or trip.get("meals", {}),
                    "popular_foods": foods[:5] or trip.get("popular_foods", []),
                    "popular_places": places[:5] or trip.get("popular_places", []),
                }
            )

    trip["destination"] = trip.get("destination") or trip_data.get("destination") or "Goa"
    trip["trip_theme"] = trip.get("trip_theme") or "Adventure, Culture & Relaxation"
    trip["best_time_to_visit"] = trip.get("best_time_to_visit") or "Nov - Feb"
    trip["hotels"] = [_normalise_hotel(hotel, index) for index, hotel in enumerate(trip.get("hotels", [])[:3])]
    trip["meals"] = {
        key: [_normalise_restaurant(item) for item in trip.get("meals", {}).get(key, [])[:2]]
        for key in ["breakfast", "lunch", "dinner"]
    }
    return trip


def render_header(trip):
    subtitle = f"{trip.get('days_count', '')} Days of {trip.get('trip_theme')}".strip()
    return f"""
    <header class="trip-header">
        <div class="trip-header-main">
            <span class="trip-header-icon">&#127796;</span>
            <div>
                <h1>Your {_html(trip["destination"])} Trip Plan</h1>
                <p>{_html(subtitle)}</p>
            </div>
        </div>
        <div class="trip-best-time">&#128197; Best time to visit: {_html(trip.get("best_time_to_visit"))}</div>
    </header>
    """


def render_hotels(hotels, recommendation, destination):
    cards = []
    for hotel in hotels:
        image = get_image("hotel", hotel["name"], hotel["location"], destination)
        badge = '<span class="trip-best-pick">Best Pick</span>' if hotel.get("is_best_pick") else ""
        price = _money(hotel.get("price_per_night"))
        cards.append(
            f"""
            <article class="trip-hotel">
                <div class="trip-hotel-image-wrap">
                    <img src="{_url(image)}" alt="{_html(hotel["name"])}">
                    {badge}
                </div>
                <div class="trip-hotel-body">
                    <h3>{_html(hotel["name"])}</h3>
                    <p class="trip-rating"><span class="star">&#9733;</span> {_html(hotel["rating"])}/5
                        <span class="reviews">({_html(_reviews(hotel.get("review_count")))})</span>
                    </p>
                    <p class="trip-location">&#128205; {_html(hotel["location"])}</p>
                    <p class="trip-price">{price} / night</p>
                    <a href="{_url(_booking_url(hotel["booking_search_query"]))}" target="_blank">View on Booking.com &#8599;</a>
                </div>
            </article>
            """
        )

    hotel_name = recommendation.get("hotel_name") or (hotels[0]["name"] if hotels else "Top hotel")
    reason = recommendation.get("reason") or "Excellent location, great reviews, and within your budget!"
    return f"""
    <section id="stays" class="trip-card trip-section">
        <div class="trip-section-title">
            <span>&#127968;</span>
            <div>
                <h2>Recommended Hotels for Your Stay</h2>
                <p class="trip-subtext">Top-rated hotels selected based on your budget &amp; preferences.</p>
            </div>
        </div>
        <div class="trip-hotels-grid">{''.join(cards)}</div>
        <div class="trip-recommendation">
            <span class="trip-recommendation-icon">&#127941;</span>
            <div>
                <strong>Our Recommendation: {_html(hotel_name)}</strong>
                <p>{_html(reason)}</p>
            </div>
        </div>
    </section>
    """


def render_day(day, destination):
    blocks = []
    for block in day.get("blocks", [])[:4]:
        title = block.get("title") or "Local experience"
        image = get_image("attraction", title, block.get("location", ""), destination)
        recommended = ""
        if block.get("recommended"):
            recommended = f'<p class="recommended">Recommended: {_html(block["recommended"])}</p>'
        location = block.get("location") or title
        maps_query = block.get("maps_query") or location
        blocks.append(
            f"""
            <section class="trip-activity">
                <h4 class="trip-activity-title">{_html(block.get("time_of_day", "Activity"))} - {_html(title)}</h4>
                <div class="trip-activity-body">
                    <img src="{_url(image)}" alt="{_html(title)}">
                    <div>
                        <p>{_html(block.get("description", ""))}</p>
                        {recommended}
                        <p class="trip-location">&#128205; {_html(location)}</p>
                        <a href="{_url(_maps_url(maps_query))}" target="_blank">View on Google Maps &#8599;</a>
                    </div>
                </div>
            </section>
            """
        )

    return f"""
    <article class="trip-card trip-day">
        <header class="trip-day-header">
            <span>&#128197;</span>
            <h3>Day {_html(day.get("day_number", ""))} - {_html(day.get("day_title", "Local Experiences"))}</h3>
        </header>
        {''.join(blocks)}
    </article>
    """


def render_dining(meals, destination):
    meal_labels = [
        ("breakfast", "&#9728;&#65039; Breakfast", "trip-meal-breakfast"),
        ("lunch", "&#9728;&#65039; Lunch", "trip-meal-lunch"),
        ("dinner", "&#127769; Dinner", "trip-meal-dinner"),
    ]
    sections = []
    for meal_key, label, class_name in meal_labels:
        rows = []
        for restaurant in meals.get(meal_key, []):
            query_name = restaurant["name"]
            image = get_image(
                "restaurant",
                query_name,
                restaurant.get("location") or restaurant.get("cuisine"),
                destination,
            )
            rows.append(
                f"""
                <article class="trip-restaurant">
                    <img src="{_url(image)}" alt="{_html(query_name)}">
                    <div>
                        <h4>{_html(query_name)}</h4>
                        <p class="trip-rating"><span class="star">&#9733;</span> {_html(restaurant["rating"])}
                            <span class="reviews">({_html(_reviews(restaurant.get("review_count")))})</span>
                        </p>
                        <p>{_html(restaurant.get("location"))}</p>
                        <p>{_html(restaurant.get("description"))}</p>
                        <p>{_html(restaurant.get("price_range")).replace("Rs", "&#8377;")}</p>
                        <a href="{_url(_maps_url(restaurant.get("maps_query") or query_name))}" target="_blank">View on Google Maps &#8599;</a>
                    </div>
                </article>
                """
            )
        if rows:
            sections.append(
                f"""
                <section class="trip-meal {class_name}">
                    <h4 class="trip-meal-label">{label}</h4>
                    {''.join(rows)}
                </section>
                """
            )

    return f"""
    <aside class="trip-card trip-dining">
        <header class="trip-dining-header">
            <span>&#127860;</span>
            <div>
                <h3>Where &amp; What to Eat</h3>
                <p class="trip-subtext">Top-rated restaurants for every meal</p>
            </div>
        </header>
        {''.join(sections)}
        <a class="trip-more-restaurants" href="{_url(_maps_url(destination + " restaurants"))}" target="_blank">
            Explore more restaurants &#8594;
        </a>
    </aside>
    """


def render_popular(foods, places, destination):
    food_name = foods[0] if foods else f"{destination} food"
    place_name = places[0].get("name", destination) if places else destination
    food_image = get_image("food", food_name, destination, destination)
    place_image = get_image("attraction", place_name, destination, destination)
    food_items = "".join(f"<li>{_html(food)}</li>" for food in foods[:5])
    place_items = "".join(
        f"""
        <li>
            <span>{_html(place.get("name", "Place"))}</span>
            <a href="{_url(_maps_url(place.get("maps_query") or place.get("name", "")))}" target="_blank">
                View on Google Maps &#8599;
            </a>
        </li>
        """
        for place in places[:5]
    )

    return f"""
    <section id="food" class="trip-bottom-grid">
        <article class="trip-card trip-popular-card">
            <div>
                <h3>&#127869;&#65039; Popular Foods to Try in {_html(destination)}</h3>
                <ul>{food_items}</ul>
            </div>
            <img src="{_url(food_image)}" alt="Popular food in {_html(destination)}">
        </article>
        <article class="trip-card trip-popular-card">
            <div>
                <h3>&#128506;&#65039; Popular Places to Explore in {_html(destination)}</h3>
                <ul class="trip-place-list">{place_items}</ul>
            </div>
            <img src="{_url(place_image)}" alt="Popular place in {_html(destination)}">
        </article>
    </section>
    """


def render_tip():
    return """
    <footer class="trip-tip">
        &#128161; <strong>Tip:</strong> Book your hotels in advance for the best prices and availability!
    </footer>
    """


def render_trip_report(trip_data, itinerary):
    trip = _normalise_trip(trip_data, itinerary or {})
    trip["days_count"] = trip_data.get("days") or len(trip.get("days", []))

    days_html = "".join(render_day(day, trip["destination"]) for day in trip.get("days", []))
    html = f"""
    {RESULT_CSS}
    <section id="trip-output" class="trip-result-page">
        {render_header(trip)}
        {render_hotels(trip.get("hotels", []), trip.get("recommendation", {}), trip["destination"])}
        <section id="itinerary" class="trip-main-grid">
            <div>{days_html}</div>
            {render_dining(trip.get("meals", {}), trip["destination"])}
        </section>
        {render_popular(trip.get("popular_foods", []), trip.get("popular_places", []), trip["destination"])}
        {render_tip()}
    </section>
    """
    st.html(html)
