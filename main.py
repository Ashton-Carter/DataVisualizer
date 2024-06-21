import streamlit as st

st.set_page_config(
    page_title="Data Visualizer",
    page_icon="📊",
)

st.sidebar.success("Select a page above.")

st.title("Data Visualizer")
st.write(
    """
    Welcome to the Data Visualizer! This application allows you to visualize various data structures and algorithms.
    """
)
