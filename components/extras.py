import streamlit as st


def render_budget_cards(trip_data, itinerary):
    st.markdown("# Budget Breakdown")

    budget = itinerary.get("budget_breakdown", {})

    if not budget:
        st.info("No budget breakdown was returned.")
        return

    cols = st.columns(len(budget))

    for col, (key, value) in zip(cols, budget.items()):
        with col:
            st.metric(key.replace("_", " ").title(), value)


def render_packing_cards(trip_data, itinerary):
    st.markdown("# Packing Checklist")

    packing = itinerary.get("packing", [])

    for item in packing:
        st.checkbox(item, value=True)


def render_tips_cards(trip_data, itinerary):
    st.markdown("# Travel Tips")

    tips = itinerary.get("travel_tips", [])

    for tip in tips:
        st.info(tip)
