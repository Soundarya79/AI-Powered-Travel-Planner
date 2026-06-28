import streamlit as st

from services.weather import get_weather


def render_hero(data, itinerary):
    weather = get_weather(data["destination"])

    col1, col2 = st.columns([5, 1])

    with col1:
        st.markdown(f"""
# Your {data['destination']} Trip Plan

##### {data['days']} Days | {data['mood']} | {", ".join(data['interests'])}
""")

        info = st.columns(4)

        info[0].metric("Travelers", data["travelers"])
        info[1].metric("Budget", f"Rs {data['budget']:,}")
        info[2].metric("Style", data["experience"])
        info[3].metric("Trip", data["trip_type"])

    with col2:
        if weather:
            st.success(
                f"""Weather

Best time: Nov - Feb

{weather['temperature']} C"""
            )
