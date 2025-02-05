import streamlit as st
import re
import logging
from data_viz.llm_integration import call_llm_for_viz, get_insights
from data_viz.utils import (
    read_uploaded_file,
    clean_dataframe,
    display_dataframe_overview,
)

# Streamlit UI
st.set_page_config(page_title="📊 AI-Powered Data Visualization", layout="wide")

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# Navigation Menu
pages = {"Data Visualization": "data_visualization", "Get Insights": "get_insights"}

# THIS DOES NOT WORK FOR SOME REASON
if st.button("🏠 Home Page", key="home_button", use_container_width=True):
    st.page_link(
        "home.py",
        label=None,
        icon=None,
        help=None,
        disabled=False,
        use_container_width=True,
    )

st.sidebar.write("#")  # Add space between home button and page selection
st.sidebar.write("#")

page = st.sidebar.selectbox("Select a page", list(pages.keys()))

st.sidebar.write("#")
st.sidebar.write("#")

# Add explore more section to sidebar
st.sidebar.markdown("---")
st.sidebar.header("🔗 Explore More")

# Add links with custom CSS for better sidebar appearance
st.sidebar.markdown(
    """
    <div style="text-align: center;">
        <a href="https://github.com/Mehyarmlaweh/DataVizQA" target="_blank">
            <img src="https://img.shields.io/badge/GitHub-Repository-blue?style=for-the-badge&logo=github" alt="GitHub">
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)


st.sidebar.markdown(
    """
    <div style="text-align: center; padding-top: 10px;">
        <a href="https://github.com/Mehyarmlaweh" target="_blank">
            <img src="https://img.shields.io/badge/Author-Mehyar_Mlaweh-black?style=for-the-badge&logo=github" alt="Mehyar">
        </a>
    </div>
    <div style="text-align: center; padding-top: 10px;">
        <a href="https://github.com/mal-mak" target="_blank">
            <img src="https://img.shields.io/badge/Author-Malek_Makhlouf-black?style=for-the-badge&logo=github" alt="Malek">
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    """
    <div style="text-align: center; padding: 10px 0;">
        <a href="https://mehyarmlaweh.github.io/DataVizQA/" target="_blank">
            <img src="https://img.shields.io/badge/Documentation-Project_Docs-orange?style=for-the-badge&logo=readthedocs" alt="Docs">
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)


# Add thank you message at bottom of sidebar
st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    <div style="text-align: center; padding: 10px;">
        ❤️ <b>Thank you for using Data Viz QA!</b>
    </div>
    """,
    unsafe_allow_html=True,
)

if page == "Data Visualization":

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

if page == "Get Insights":
    st.title("📷 Get Insights")
    st.markdown("Upload a plot or image to get insights on it.(PNG ONLY)")

    uploaded_image = st.file_uploader(
        "📂 Upload an image", type=["jpg", "jpeg", "png"]
    )  # ?? NOT ONLY PNG ??

    if uploaded_image:
        st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)

        with st.spinner("⏳ Generating visualization code..."):
            insights = get_insights(uploaded_image)

        # Display insights
        st.subheader("🔍 Insights")
        st.write(insights)
