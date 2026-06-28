from urllib.parse import quote

import streamlit as st

from services.images import get_image


def render_food_cards(trip_data, itinerary):
    st.markdown("# Must Try Local Foods")

    foods = itinerary.get("must_try_food", [])

    if not foods:
        st.info("No local food recommendations were returned.")
        return

    cols = st.columns(3)

    for col, food in zip(cols, foods):
        with col:
            image = get_image(food.get("image_query", food.get("name", "food")))

            if image:
                st.image(image, use_container_width=True)

            st.subheader(food.get("name", "Food"))
            st.write(food.get("about", ""))
            st.write(f"Best Restaurant: {food.get('best_restaurant', '')}")

            maps = (
                "https://www.google.com/maps/search/?api=1&query="
                + quote(food.get("best_restaurant", food.get("name", "")))
            )

            st.link_button("Where to Eat", maps, use_container_width=True)
