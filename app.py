from datetime import date, timedelta
from pathlib import Path
import streamlit as st
from ai.itinerary import generate_itinerary
from components.trip_report import render_trip_report

st.set_page_config(
    page_title="VoyageAI | AI Travel Planner",
    page_icon="V",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def load_css(file_name: str) -> None:
    css_path = Path(__file__).parent / file_name
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)


def money(value: int) -> str:
    return f"Rs {value:,.0f}"


def image_card(title: str, text: str, tag: str, class_name: str) -> None:
    st.markdown(
        f"""
        <article class="image-card {class_name}">
            <div class="image-card-overlay">
                <span>{tag}</span>
                <h3>{title}</h3>
                <p>{text}</p>
            </div>
        </article>
        """,
        unsafe_allow_html=True,
    )


def simple_card(title: str, text: str, tag: str = "") -> None:
    tag_html = f"<span>{tag}</span>" if tag else ""
    st.markdown(
        f"""
        <article class="simple-card">
            {tag_html}
            <h3>{title}</h3>
            <p>{text}</p>
        </article>
        """,
        unsafe_allow_html=True,
    )


load_css("styles.css")

st.markdown(
    """
    <header class="site-nav">
        <a class="logo" href="#">
            <span>V</span>
            <strong>VoyageAI</strong>
        </a>
        <nav>
            <a href="#planner">Planner</a>
            <a href="#itinerary">Itinerary</a>
            <a href="#stays">Stays</a>
            <a href="#food">Food</a>
        </nav>
    </header>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="website-hero">
        <div class="hero-content">
            <span class="hero-kicker">AI travel planner</span>
            <h1>Plan your next trip like a real travel expert.</h1>
            <p>
                Build a complete itinerary with routes, hotel areas, local food,
                attractions, budget guidance, and day-wise plans.
            </p>
            <div class="hero-actions">
                <a href="#planner">Start planning</a>
                <span>Inspired by modern travel search experiences</span>
            </div>
        </div>
        <div class="hero-panel">
            <span>Popular plan</span>
            <strong>Goa beach escape</strong>
            <p>5 days, food trail, scenic drives, stays near the coast.</p>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

#st.markdown('<section id="planner" class="booking-shell">', unsafe_allow_html=True)
st.markdown(
    """
    <div class="section-heading">
        <h2>Where should VoyageAI take you?</h2>
        <p>Fill the details once. The page below turns into a complete travel website for your trip.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form("trip_form"):
    first_row = st.columns([1, 1, 0.7, 0.7])
    with first_row[0]:
        source = st.text_input("Source City", placeholder="Mumbai")
    with first_row[1]:
        destination = st.text_input("Destination", placeholder="Goa")
    with first_row[2]:
        start_date = st.date_input("Start Date", value=date.today())
    with first_row[3]:
        days = st.number_input("Number of Days", min_value=1, max_value=30, value=3)

    second_row = st.columns([0.8, 0.8, 0.9, 0.9])
    with second_row[0]:
        budget = st.number_input("Budget (Rs)", min_value=1000, step=1000, value=25000)
    with second_row[1]:
        travelers = st.number_input("Number of Travelers", min_value=1, max_value=10, value=1)
    with second_row[2]:
        travel_style = st.selectbox("Travel Style", ["Budget", "Comfort", "Luxury"])
    with second_row[3]:
        trip_type = st.selectbox("Trip Type", ["Solo", "Couple", "Family", "Friends"])

    third_row = st.columns([0.9, 1.4, 0.7])
    with third_row[0]:
        trip_mood = st.selectbox(
            "Trip Mood",
            ["Relax", "Adventure", "Romantic", "Family Time", "Explore", "Party"],
        )
    with third_row[1]:
        interests = st.multiselect(
            "Interests",
            [
                "Beaches",
                "Mountains",
                "Adventure",
                "Nature",
                "Food",
                "History",
                "Shopping",
                "Nightlife",
                "Wildlife",
                "Spiritual",
            ],
            default=["Food", "Nature"],
        )
    with third_row[2]:
        pace = st.select_slider(
            "Trip Pace",
            options=["Slow", "Balanced", "Packed"],
            value="Balanced",
        )

    generate = st.form_submit_button("Generate my trip", use_container_width=True)

st.markdown("</section>", unsafe_allow_html=True)

destination_label = destination.strip() or "Goa"
source_label = source.strip() or "Mumbai"
per_person = budget // travelers if travelers else budget
daily_budget = budget // int(days) if days else budget
end_date = start_date + timedelta(days=int(days) - 1)

if generate and (not source.strip() or not destination.strip()):
    st.warning("Please enter both Source City and Destination.")

elif generate:
    trip_data = {
        "source": source.strip(),
        "destination": destination.strip(),
        "days": int(days),
        "budget": int(budget),
        "travelers": int(travelers),
        "experience": travel_style,
        "trip_type": trip_type,
        "mood": trip_mood,
        "interests": interests,
        "pace": pace,
        "start_date": start_date.isoformat(),
    }

    with st.spinner("Generating your AI travel plan..."):
        try:
            itinerary = generate_itinerary(trip_data)
        except Exception as e:
            st.error(e)
            st.stop()

    st.success("Trip generated successfully!")

    render_trip_report(trip_data, itinerary)
