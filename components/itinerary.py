from urllib.parse import quote

import streamlit as st

from services.images import get_image


def get_place(slot):
    if isinstance(slot, list):
        slot = slot[0] if slot else {}

    if not isinstance(slot, dict):
        return {}

    return slot.get("place", slot)


def place_card(title, place):
    place_name = place.get("name") or place.get("place") or "Place"
    image = get_image(place.get("image_query", place_name))

    left, right = st.columns([1, 2])

    with left:
        if image:
            st.image(image, use_container_width=True)

    with right:
        st.markdown(f"## {title}")
        st.markdown(f"### {place_name}")

        if place.get("about"):
            st.write(place["about"])
        else:
            st.write(place.get("reason", ""))

        c1, c2 = st.columns(2)

        with c1:
            st.write(f"**Best Time:** {place.get('best_time', place.get('time', ''))}")
            st.write(f"**Duration:** {place.get('duration', '')}")
            st.write(f"**Entry Fee:** {place.get('entry_fee', '')}")

        with c2:
            st.write(f"**Travel:** {place.get('travel_time', '')}")
            st.write("**Why Visit:**")
            st.write(place.get("why_visit", place.get("reason", "")))

        maps = (
            "https://www.google.com/maps/search/?api=1&query="
            + quote(place.get("google_maps_search", place_name))
        )

        st.link_button("Open in Google Maps", maps, use_container_width=True)

    st.markdown("---")


def render_day_cards(trip_data, itinerary):
    st.markdown("# Day-wise Itinerary")

    for day in itinerary.get("itinerary", []):
        st.markdown(f"# Day {day.get('day', '')}")
        st.success(day.get("theme", ""))

        place_card("Morning", get_place(day.get("morning", {})))
        place_card("Afternoon", get_place(day.get("afternoon", {})))
        place_card("Evening", get_place(day.get("evening", {})))

        st.divider()
