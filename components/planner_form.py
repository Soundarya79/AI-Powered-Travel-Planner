import streamlit as st


def show_planner_form():

    st.markdown("# 🧳 Plan Your Journey")

    col1, col2 = st.columns(2)

    with col1:

        source = st.text_input("📍 Source City")

        destination = st.text_input("🌍 Destination")

        start_date = st.date_input("📅 Start Date")

        days = st.number_input(
            "📆 Number of Days",
            min_value=1,
            max_value=30,
            value=3
        )

    with col2:

        budget = st.number_input(
            "💰 Trip Budget (₹)",
            min_value=1000,
            step=1000
        )

        travelers = st.number_input(
            "👨‍👩‍👧 Number of Travelers",
            min_value=1,
            max_value=20,
            value=1
        )

        experience = st.selectbox(
            "🏨 Travel Experience",
            [
                "Budget",
                "Comfort",
                "Luxury"
            ]
        )

        trip_type = st.selectbox(
            "👥 Who's Traveling?",
            [
                "Solo",
                "Couple",
                "Family",
                "Friends"
            ]
        )

    mood = st.selectbox(
        "✨ Trip Mood",
        [
            "Relax",
            "Adventure",
            "Romantic",
            "Family Time",
            "Explore",
            "Party"
        ]
    )

    interests = st.multiselect(
        "🎯 What excites you?",
        [
            "Food",
            "Nature",
            "Adventure",
            "History",
            "Shopping",
            "Nightlife",
            "Beaches",
            "Wildlife",
            "Photography",
            "Culture"
        ]
    )

    generate = st.button(
        "🚀 Generate My Adventure",
        use_container_width=True
    )

    return {
        "source": source,
        "destination": destination,
        "start_date": start_date,
        "days": days,
        "budget": budget,
        "travelers": travelers,
        "experience": experience,
        "trip_type": trip_type,
        "mood": mood,
        "interests": interests,
        "generate": generate
    }