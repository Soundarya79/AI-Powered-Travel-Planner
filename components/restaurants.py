from urllib.parse import quote

import streamlit as st

from services.images import get_image


def get_restaurant(slot):
    if isinstance(slot, list):
        slot = slot[0] if slot else {}

    if not isinstance(slot, dict):
        return {}

    return slot.get("restaurant", slot)


def restaurant_card(title, restaurant):
    restaurant_name = (
        restaurant.get("name")
        or restaurant.get("restaurant")
        or "Restaurant"
    )
    image = get_image(restaurant.get("image_query", restaurant_name))

    left, right = st.columns([1, 2])

    with left:
        if image:
            st.image(image, use_container_width=True)

    with right:
        st.markdown(f"## {title}")
        st.markdown(f"### {restaurant_name}")
        st.write(f"**Cuisine:** {restaurant.get('cuisine', '')}")
        st.write(f"**Must Try:** {restaurant.get('must_try', restaurant.get('food', ''))}")
        st.write(f"**Cost:** {restaurant.get('cost_for_two', restaurant.get('cost', ''))}")

        maps = (
            "https://www.google.com/maps/search/?api=1&query="
            + quote(restaurant.get("google_maps_search", restaurant_name))
        )

        st.link_button("Open in Google Maps", maps, use_container_width=True)

    st.markdown("---")


def render_restaurants(trip_data, itinerary):
    st.markdown("# Recommended Restaurants")

    for day in itinerary.get("itinerary", []):
        st.markdown(f"## Day {day.get('day', '')}")

        if day.get("morning"):
            restaurant_card("Breakfast", get_restaurant(day.get("morning", {})))

        if day.get("afternoon"):
            restaurant_card("Lunch", get_restaurant(day.get("afternoon", {})))

        if day.get("night"):
            restaurant_card("Dinner", get_restaurant(day.get("night", {})))
