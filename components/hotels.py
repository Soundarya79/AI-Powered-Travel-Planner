import streamlit as st
from services.images import get_image
from urllib.parse import quote


def render_hotels(trip_data, itinerary):

    st.markdown("## 🏨 Recommended Hotels")

    budget = trip_data["budget"]

    if budget < 10000:
        hotels = itinerary["hotels"]["budget"]
    elif budget < 30000:
        hotels = itinerary["hotels"]["comfort"]
    else:
        hotels = itinerary["hotels"]["luxury"]

    cols = st.columns(3)

    for col, hotel in zip(cols, hotels):

        with col:

            image = get_image(
                hotel.get("image_query", hotel["name"])
            )

            if image:
                st.image(image, use_container_width=True)

            st.subheader(hotel["name"])

            st.write(f"⭐ {hotel['rating']}")

            st.write(f"💰 {hotel['price_per_night']} / night")

            st.write(f"📍 {hotel['location']}")

            st.info(hotel["why"])

            maps = (
                "https://www.google.com/maps/search/?api=1&query="
                + quote(
                    hotel.get(
                        "google_maps_search",
                        hotel["name"] + " " + hotel["location"],
                    )
                )
            )

            booking = (
                "https://www.booking.com/searchresults.html?ss="
                + quote(
                    hotel.get(
                        "booking_search",
                        hotel["name"],
                    )
                )
            )

            c1, c2 = st.columns(2)

            with c1:
                st.link_button(
                    "📍 Maps",
                    maps,
                    use_container_width=True,
                )

            with c2:
                st.link_button(
                    "🏨 Booking",
                    booking,
                    use_container_width=True,
                )