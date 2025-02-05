import streamlit as st
import pandas as pd
import re
import tempfile
import logging
from llm_integration import call_llm_for_viz, get_insights
import matplotlib.pyplot as plt
from utils import (
    read_uploaded_file,
    clean_dataframe,
    display_dataframe_overview,
)
# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def load_data(file):
    """Load uploaded file into a DataFrame."""
    try:
        if file.name.endswith(".csv"):
            return pd.read_csv(file)
        return pd.read_excel(file)
    except Exception as e:
        st.error("🚨 Error loading file. Please upload a valid CSV or Excel file.")
        logger.error(f"🚨 Error loading file: {e}")
        return None

def clean_data(df):
    """Clean the dataset."""
    # Example cleaning: drop duplicates and handle missing values
    df_cleaned = df.drop_duplicates().dropna()
    return df_cleaned

# Streamlit UI
st.set_page_config(page_title="📊 AI-Powered Data Visualization", layout="wide")
# Navigation Menu
pages = {
    "Home" : "home",
    "Data Visualization": "data_visualization",
    "Get Insights": "get_insights"
}

page = st.sidebar.selectbox("Select a page", list(pages.keys()))

if page == "Home":
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
elif page == "Data Visualization":

    st.title("📊 AI-Powered Data Visualization")
    st.markdown("🚀 Generate insightful visualizations using AI-powered suggestions!")
    st.header("📂 Upload Your Dataset")
    uploaded_file = st.file_uploader(" Upload a CSV or Excel file", type=["csv", "xlsx"], key="file_upload")

    if uploaded_file:
        df = load_data(uploaded_file)
        if df is not None:
            st.subheader("🔍 Data Preview")
            st.dataframe(df.head())

            # Data Cleaning Section
            if st.button("🧹🧹 Clean Dataset"):
                df_cleaned = clean_data(df)
                st.success("Dataset cleaned successfully!")
                st.dataframe(df_cleaned.head())
                df = df_cleaned  # Update the DataFrame to the cleaned version

            st.subheader("📈 Dataset Summary")
            st.write(df.describe())

            user_prompt = st.text_area(
                "📝 Describe the visualization you want:",
                placeholder="Example: Show a bar chart of categorical data"
            )

            if st.button("🚀 Generate Visualization"):
                if user_prompt.strip():
                    with st.spinner("⏳ Generating visualization code..."):
                        generated_code = call_llm_for_viz(df, user_prompt)
                        st.subheader("🖥 Generated Code")
                        st.code(generated_code, language="python")
                        match = re.search(r"```python\n(.*?)\n```", generated_code, re.DOTALL)
                        
                        if match:
                            python_code = match.group(1)
                            safe_code = python_code.replace("plt.show()", "st.pyplot(plt)")
                            st.subheader("📊 Visualization")
                            try:
                                if safe_code:
                                    exec(safe_code, globals())                                
                                st.markdown("💡 **Kindly save this plot to get insights on it from the section Get Insights.**")
                            
                            except Exception as e:
                                st.error(f"⚠️ Error executing visualization: {e}")
                                logger.error(f"⚠️ Error executing visualization: {e}")
                        elif generated_code:
                            try:
                                exec(generated_code, globals())
                                st.markdown("💡 **Kindly save this plot to get insights on it from the section Get Insights.**")
                            except Exception as e:
                                st.error(f"⚠️ Error executing visualization: {e}")
                                logger.error(f"⚠️ Error executing visualization: {e}")
                        else :
                            st.warning("⚠️ No valid Python code detected in the response.")

                else:
                    st.warning("⚠️ Please describe the visualization you want.")
    else:
        st.info("📂 Upload a file to get started!")

if page == "Get Insights":
    st.title("📷 Get Insights")
    st.header("📂 Upload a plot or image to get insights on it")
    st.markdown("Supported Type : PNG")

    uploaded_image = st.file_uploader("📂 Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image:
        st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)

        with st.spinner("⏳ Generating visualization code..."):
            insights = get_insights(uploaded_image)

        # Display insights
        st.subheader("🔍 Insights")
        st.write(insights)


