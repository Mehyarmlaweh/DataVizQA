"""
Main module for the AI-Powered Data Visualization application.
This module handles the application's routing and main page structure.
It provides navigation between different pages:
- Home page
- Data Visualization page
- Insights page
"""

import streamlit as st
from home import home_page, explore_more
from chat import data_viz_chat_page
from insights import get_insights_page


def main():
    """
    Main function that sets up the Streamlit application interface.
    Handles page routing and navigation menu setup.
    
    Returns:
        None. Renders the application directly using Streamlit.
    """
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


if __name__ == "__main__":
    main()
