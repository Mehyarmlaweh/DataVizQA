import streamlit as st
import pandas as pd
from data_viz.utils import (
    read_uploaded_file,
    clean_dataframe,
    display_dataframe_overview,
    footer,
)

# Apply a custom Streamlit theme
st.set_page_config(page_title="Data Viz QA", page_icon="📊", layout="wide")


def main():
    """
    Home page for the DataVizQA project.
    Features:
    - File upload with overview functionality.
    """
    # Title section
    st.title("📊 Data Viz QA")
    st.markdown(
        """
        ### Empower Your Data with Intuitive Insights and Visualizations!  
        **Data Viz QA** is a collaborative effort to make data exploration effortless. Upload your dataset, ask questions, and receive stunning visualizations along with meaningful insights.
        """
    )

    st.markdown("---")

    # Create a row of columns (1 for the content, 2 for the button)
    col1, col2 = st.columns([4, 1])  # Adjust the ratio to get the button on the right side

    with col1:
        # Project description
        st.header("🔍 About the Project")
        st.write(
            """
            **Data Viz QA** simplifies data interaction by allowing you to:
            - Upload tabular datasets (CSV, Excel).
            - Ask natural language questions about your data.
            - Receive tailored visualizations and interpretations.
            
            The project leverages advanced large language models like GPT or Claude to understand your queries and provide actionable insights.
            """
        )

    with col2:
        # Button to navigate to the chat page (replace the link with the actual chat page link) !!!!!!!!!!!!!!!!!!!!!!!!!
        st.markdown(
            """
            <a href="https://github.com/Mehyarmlaweh" target="_self">
                <button style="padding: 30px; background-color: #4CAF50; color: white; border: none; border-radius: 12px; cursor: pointer; width: 300px; height: 300px; text-align: center; font-size: 22px;">
                    Go to Chat Page
                </button>
            </a>
            """, 
            unsafe_allow_html=True
        )

    # Dataset upload
    st.header("📂 Upload Your Dataset")
    st.write("Drag and drop a file or select one using the file picker below:")
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])

    if uploaded_file:
        # Initialize session state for storing DataFrames if not exists
        if "raw_df" not in st.session_state:
            st.session_state.raw_df = None
        if "cleaned_df" not in st.session_state:
            st.session_state.cleaned_df = None

        # Read the file if it hasn't been read yet
        if st.session_state.raw_df is None:
            st.session_state.raw_df = read_uploaded_file(uploaded_file)

        if st.session_state.raw_df is not None:
            col1, col2 = st.columns([1, 2])

            with col1:
                if st.button("🧹 Clean Data"):
                    st.session_state.cleaned_df = clean_dataframe(
                        st.session_state.raw_df
                    )
                    st.success("Data cleaned successfully!")

            with col2:
                show_cleaned = st.toggle(
                    "Show cleaned data",
                    value=False,
                    disabled=st.session_state.cleaned_df is None,
                )

            # Display either raw or cleaned data based on toggle state
            if show_cleaned and st.session_state.cleaned_df is not None:
                display_dataframe_overview(st.session_state.cleaned_df)
                st.info("Showing cleaned data")
            else:
                display_dataframe_overview(st.session_state.raw_df)
                st.info("Showing raw data")

    footer()


if __name__ == "__main__":
    main()
