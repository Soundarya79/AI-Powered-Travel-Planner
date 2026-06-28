import streamlit as st


def start_page():

    st.markdown(
        """
        <div class="trip-container">
        """,
        unsafe_allow_html=True,
    )


def end_page():

    st.markdown(
        """
        </div>
        """,
        unsafe_allow_html=True,
    )