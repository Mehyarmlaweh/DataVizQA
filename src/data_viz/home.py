import streamlit as st

# Apply a custom Streamlit theme
st.set_page_config(
    page_title="Data Viz QA",
    page_icon="📊",
    layout="wide"
)


def main():
    """
    Enhanced home page for the DataVizQA project.
    Features:
    - Modern design with custom themes.
    - Sections for better navigation.
    - Interactive buttons for repository and documentation links.
    """
    # Title section
    st.title("📊 Data Viz QA")
    st.markdown(
        """
        ### Empower Your Data with Intuitive Insights and Visualizations!  
        **Data Viz QA** is a collaborative effort to make data exploration effortless. Upload your dataset, ask questions, and receive stunning visualizations along with meaningful insights.
        """
    )

    # Add a horizontal divider
    st.markdown("---")

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

    # Dataset upload placeholder
    st.header("📂 Upload Your Dataset")
    st.write("Drag and drop a file or select one using the file picker below:")
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])
    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")

    # External links as buttons
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
            [![Demo](https://img.shields.io/badge/Another_Page-Demo-green?style=for-the-badge&logo=streamlit)](#)
            """
        )

    # Footer section
    st.markdown("---")
    st.write(
        """
        ❤️ **Thank you for using Data Viz QA!**
        """
    )


if __name__ == "__main__":
    main()