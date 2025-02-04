import streamlit as st
import pandas as pd
import re
import tempfile
import logging
from data_viz.llm_integration import call_llm_for_viz, get_insights
import matplotlib.pyplot as plt

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
    "Data Visualization": "data_visualization",
    "Get Insights": "get_insights"
}

page = st.sidebar.selectbox("Select a page", list(pages.keys()))

if page == "Data Visualization":

    st.title("📊 AI-Powered Data Visualization")
    st.markdown("🚀 Generate insightful visualizations using AI-powered suggestions!")

    uploaded_file = st.file_uploader("📂 Upload a CSV or Excel file", type=["csv", "xlsx"], key="file_upload")

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
    st.markdown("Upload a plot or image to get insights on it.(PNG ONLY)")

    uploaded_image = st.file_uploader("📂 Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image:
        st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)

        with st.spinner("⏳ Generating visualization code..."):
            insights = get_insights(uploaded_image)

        # Display insights
        st.subheader("🔍 Insights")
        st.write(insights)


