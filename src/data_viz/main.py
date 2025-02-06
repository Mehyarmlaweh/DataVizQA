import streamlit as st
from data_viz.home import home_page, explore_more
from data_viz.chat import data_viz_chat_page
from data_viz.insights import get_insights_page


# Streamlit UI
st.set_page_config(page_title="📊 AI-Powered Data Visualization", layout="wide")

# Navigation Menu
pages = {
    "Home": "home",
    "Data Visualization": "data_visualization",
    "Get Insights": "get_insights",
}

page = st.sidebar.selectbox("Select a page", list(pages.keys()))

if page == "Home":
    home_page()

elif page == "Data Visualization":
    data_viz_chat_page()

elif page == "Get Insights":
    get_insights_page()

# Footer (Explore More)
explore_more()
