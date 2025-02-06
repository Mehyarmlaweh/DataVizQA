import streamlit as st
from utils import (
    read_uploaded_file,
    clean_dataframe,
    display_dataframe_overview,
)

def explore_more():
    """
    Display the explore more section of the application with links to GitHub repository,
    documentation, and authors information.
    
    This function creates a section with three columns containing:
    - GitHub repository link
    - Documentation link
    - Author information links
    It also includes a thank you message at the bottom.
    """
    # Explore more
    st.markdown("---")
    st.header("🔗 Explore More")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            [![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?style=for-the-badge&logo=github)](https://github.com/Mehyarmlaweh/DataVizQA)
            """
        )

    with col2:
        st.markdown(
            """
            [![Docs](https://img.shields.io/badge/Documentation-Project_Docs-orange?style=for-the-badge&logo=readthedocs)](#)
            """
        )
    with col3:
        st.markdown(
            """
            [![Author](https://img.shields.io/badge/Author-Mehyar_Mlaweh-black?style=for-the-badge&logo=github)](https://github.com/Mehyarmlaweh) 
            [![Author](https://img.shields.io/badge/Author-Malek_Makhlouf-black?style=for-the-badge&logo=github)](https://github.com/mal-mak)
            """
        )

    # Footer thank-you message
    st.markdown("---")
    st.write(
        """
        ❤️ **Thank you for using Data Viz QA!**
        """
    )

def home_page():
    """
    Display the main home page of the DataVizQA application.
    
    Features:
    - Displays project title and description
    - Provides file upload functionality for CSV and Excel files
    - Offers data cleaning capabilities
    - Shows data overview with toggle between raw and cleaned data
    
    The function manages the session state to store both raw and cleaned
    versions of the uploaded dataset.
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
    col1, col2 = st.columns(
        [4, 1]
    )  # Adjust the ratio to get the button on the right side

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
        pass

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
