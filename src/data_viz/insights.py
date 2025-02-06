import streamlit as st
from llm_integration import get_insights

def get_insights_page():
    """
    Renders the insights page with image upload functionality and analysis results.

    The page allows users to:
    - Enter their API key for the LLM service
    - Upload PNG images
    - View the uploaded image
    - Get AI-generated insights about the visualization

    Returns:
        None. Renders the page content directly using Streamlit.
    """
    st.title("📷 Get Insights")
    st.header("📂 Upload a plot or image to get insights on it")
    st.markdown("Supported Types: JPG, JPEG, PNG")

    # Add a text input for the user's API key
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""

    st.session_state.api_key = st.text_input(
        "🔑 Enter your Claude API Key (from Anthropic):",
        value=st.session_state.api_key,
        type="password",  # Mask the input for security
    )

    if not st.session_state.api_key.strip():
        st.warning("⚠️ Please enter a valid API key to proceed.")
        return

    uploaded_image = st.file_uploader("📂 Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image:
        st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)

        with st.spinner("⏳ Generating insights..."):
            try:
                # Pass the API key to the get_insights function
                insights = get_insights(uploaded_image, API_KEY=st.session_state.api_key)
                
                # Display insights
                st.subheader("🔍 Insights")
                st.write(insights)
            except Exception as e:
                st.error(f"⚠️ Error generating insights: {e}")