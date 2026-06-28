import streamlit as st


def show_results(data):

    st.success("🎉 Your adventure is ready!")

    if isinstance(data, str):
        st.markdown(data, unsafe_allow_html=True)
    else:
        st.write(data)