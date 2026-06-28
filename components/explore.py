from urllib.parse import quote

import streamlit as st

from services.images import get_image


def render_explore_cards(trip_data, itinerary):
    st.markdown("# Must Visit Places")

    places = itinerary.get("must_visit", [])

    if not places:
        st.info("No must-visit places were returned.")
        return

    cols = st.columns(3)

    for col, place in zip(cols, places):
        with col:
            image = get_image(place.get("image_query", place.get("name", "place")))

            if image:
                st.image(image, use_container_width=True)

            st.subheader(place.get("name", "Place"))
            st.write(place.get("about", ""))
            st.write(f"Best Time: {place.get('best_time', '')}")

            maps = (
                "https://www.google.com/maps/search/?api=1&query="
                + quote(place.get("google_maps_search", place.get("name", "")))
            )

            st.link_button("Open in Google Maps", maps, use_container_width=True)
