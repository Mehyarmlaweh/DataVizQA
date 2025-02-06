import streamlit as st
from data_viz.llm_integration import get_insights


def get_insights_page():
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
