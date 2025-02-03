import streamlit as st
import pandas as pd
import re
import logging
from llm_integration import call_llm_for_viz

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
        st.error("Error loading file. Please upload a valid CSV or Excel file.")
        logger.error(f"Error loading file: {e}")
        return None

# Streamlit UI
st.set_page_config(page_title="AI-Powered Data Visualization", layout="wide")

# Add Dark Mode Toggle
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode

st.sidebar.title("⚙️ Settings")
st.sidebar.button("🌙 Toggle Dark Mode", on_click=toggle_dark_mode)

# Apply Dark Mode Styling
if st.session_state.dark_mode:
    st.markdown(
        """
        <style>
        body {
            background-color: #1e1e1e;
            color: white;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

st.title("📊 AI-Powered Data Visualization")
st.markdown("Generate insightful visualizations using AI-powered suggestions!")

uploaded_file = st.file_uploader("📂 Upload a CSV or Excel file", type=["csv", "xlsx"], key="file_upload")

if uploaded_file:
    df = load_data(uploaded_file)
    if df is not None:
        st.subheader("🔍 Data Preview")
        st.dataframe(df.head())

        st.subheader("📈 Dataset Summary")
        st.write(df.describe())

        user_prompt = st.text_area(
            "📝 Describe the visualization you want:",
            placeholder="Example: Show a bar chart of categorical data"
        )

        if st.button("🚀 Generate Visualization"):
            if user_prompt.strip():
                with st.spinner("Generating visualization code..."):
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
                            else:
                                exec(python_code, globals()) 
                        except Exception as e:
                            st.error(f"⚠️ Error executing visualization: {e}")
                            logger.error(f"Error executing visualization: {e}")
                    else:
                        st.warning("⚠️ No valid Python code detected in the response.")
            else:
                st.warning("⚠️ Please describe the visualization you want.")
else:
    st.info("Upload a file to get started!")