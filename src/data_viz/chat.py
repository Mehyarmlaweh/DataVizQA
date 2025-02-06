import streamlit as st
import re
import logging
from llm_integration import call_llm_for_viz
from utils import (
    read_uploaded_file,
    clean_dataframe,
    display_dataframe_overview,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def data_viz_chat_page():
    """
    Renders the main data visualization chat interface page in Streamlit.
    
    This function provides the following features:
    - File upload interface for CSV and Excel files
    - Data cleaning capabilities with toggle to view raw/cleaned data
    - Dataset overview and summary statistics
    - Natural language interface for visualization generation
    - Code generation and visualization rendering
    
    The function maintains the state of both raw and cleaned DataFrames using
    Streamlit's session state, ensuring persistence across reruns.
    
    Returns:
        None. All output is rendered directly to the Streamlit interface.
    
    Raises:
        Various exceptions may be caught and displayed in the Streamlit UI,
        particularly during visualization generation and execution.
    """
    
    st.title("📊 AI-Powered Data Visualization")
    st.markdown("🚀 Generate insightful visualizations using AI-powered suggestions!")

    df = None
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
            df = st.session_state.raw_df

        if st.session_state.raw_df is not None:
            col1, col2 = st.columns([1, 2])

            with col1:
                if st.button("🧹 Clean Data"):
                    st.session_state.cleaned_df = clean_dataframe(
                        st.session_state.raw_df
                    )
                    df = st.session_state.cleaned_df
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
                st.write("### 📈 Dataset Summary")
                st.write(st.session_state.cleaned_df.describe())
                st.info("Showing cleaned data")
                df = st.session_state.cleaned_df
            else:
                display_dataframe_overview(st.session_state.raw_df)
                st.write("### 📈 Dataset Summary")
                st.write(st.session_state.raw_df.describe())
                st.info("Showing raw data")
                df = st.session_state.raw_df

    user_prompt = st.text_area(
        "📝 Describe the visualization you want:",
        placeholder="Example: Show a bar chart of categorical data",
    )
    if st.button("🚀 Generate Visualization"):
        if df is not None:
            if user_prompt.strip():
                with st.spinner("⏳ Generating visualization code..."):

                    generated_code = call_llm_for_viz(df, user_prompt)
                    st.subheader("🖥 Generated Code")
                    st.code(generated_code, language="python")
                    match = re.search(
                        r"```python\n(.*?)\n```", generated_code, re.DOTALL
                    )

                    if match:
                        python_code = match.group(1)
                        safe_code = python_code.replace("plt.show()", "st.pyplot(plt)")
                        st.subheader("📊 Visualization")
                        try:
                            if safe_code:
                                exec(safe_code, globals())
                            st.markdown(
                                "💡 **Kindly save this plot to get insights on it from the section Get Insights.**"
                            )

                        except Exception as e:
                            st.error(f"⚠️ Error executing visualization: {e}")
                            logger.error(f"⚠️ Error executing visualization: {e}")
                    elif generated_code:
                        try:
                            exec(generated_code, globals())
                            st.markdown(
                                "💡 **Kindly save this plot to get insights on it from the section Get Insights.**"
                            )
                        except Exception as e:
                            st.error(f"⚠️ Error executing visualization: {e}")
                            logger.error(f"⚠️ Error executing visualization: {e}")
                    else:
                        st.warning("⚠️ No valid Python code detected in the response.")

            else:
                st.warning("⚠️ Please describe the visualization you want.")
        else:
            st.error("⚠️ Please upload a file to generate visualizations.")
    else:
        if uploaded_file is None:
            st.info("📂 Upload a file to get started!")
