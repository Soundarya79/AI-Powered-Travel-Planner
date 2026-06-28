from urllib.parse import quote

import streamlit as st

from services.images import get_image


def render_hotels(trip_data, itinerary):
    hotels_data = itinerary.get("hotels", {})
    if isinstance(hotels_data, dict):
        hotels = hotels_data.get("recommended", [])
    else:
        hotels = hotels_data

    st.markdown("## Recommended Hotels for Your Stay")
    st.caption("Top-rated hotels selected based on your budget and preferences.")

    if not hotels:
        st.info("No hotel recommendations were returned.")
        return

    cols = st.columns(3)

    for col, hotel in zip(cols, hotels[:3]):
        with col:
            image = get_image(hotel.get("image_query") or hotel.get("name", "hotel"))

            if image:
                st.image(image, use_container_width=True)

            st.markdown(f"### {hotel.get('name', 'Hotel')}")
            st.write(f"Rating: {hotel.get('rating', '')}")
            st.write(f"Location: {hotel.get('location', '')}")
            st.write(f"Price: **{hotel.get('price_per_night', '')}**")
            st.caption(hotel.get("why", ""))

            maps = (
                "https://www.google.com/maps/search/?api=1&query="
                + quote(
                    hotel.get(
                        "google_maps_search",
                        f"{hotel.get('name', '')} {hotel.get('location', '')}",
                    )
                )
            )
            booking = (
                "https://www.booking.com/searchresults.html?ss="
                + quote(hotel.get("booking_search", hotel.get("name", "")))
            )

            c1, c2 = st.columns(2)

            with c1:
                st.link_button("Maps", maps)

            with c2:
                st.link_button("Booking", booking)
