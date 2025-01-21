import streamlit as st
import pandas as pd


def footer():
    """
    Displays the footer section with external links and a thank-you message.
    """
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

    # Footer thank-you message
    st.markdown("---")
    st.write(
        """
        ❤️ **Thank you for using Data Viz QA!**
        """
    )


def read_uploaded_file(uploaded_file):
    """
    Read the uploaded file into a pandas DataFrame.

    Parameters:
    uploaded_file: Streamlit UploadedFile object

    Returns:
    pd.DataFrame or None if error occurs
    """
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith((".xls", ".xlsx")):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload a CSV or Excel file.")
            return None
        return df
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return None


def clean_dataframe(df):
    """
    Clean the input DataFrame.

    Parameters:
    df: pandas DataFrame

    Returns:
    pd.DataFrame: Cleaned DataFrame
    """
    # Make a copy to avoid modifying original data
    df_cleaned = df.copy()

    # Clean column names
    df_cleaned.columns = df_cleaned.columns.str.strip()
    df_cleaned.columns = df_cleaned.columns.str.lower()
    df_cleaned.columns = df_cleaned.columns.str.replace(" ", "_")
    df_cleaned.columns = df_cleaned.columns.str.replace(r"[^\w\s]", "")

    # Remove duplicate rows
    initial_rows = len(df_cleaned)
    df_cleaned = df_cleaned.drop_duplicates()
    if len(df_cleaned) < initial_rows:
        st.warning(f"Removed {initial_rows - len(df_cleaned)} duplicate rows")

    # Handle missing values
    for column in df_cleaned.columns:
        missing_count = df_cleaned[column].isnull().sum()
        if missing_count > 0:
            if pd.api.types.is_numeric_dtype(df_cleaned[column]):
                df_cleaned[column] = df_cleaned[column].fillna(
                    df_cleaned[column].median()
                )
            else:
                df_cleaned[column] = df_cleaned[column].fillna(
                    df_cleaned[column].mode()[0]
                )
            st.info(f"Filled {missing_count} missing values in column '{column}'")

    # Strip whitespace from string columns
    for column in df_cleaned.select_dtypes(include=["object"]):
        df_cleaned[column] = df_cleaned[column].str.strip()

    return df_cleaned


def display_dataframe_overview(df):
    """
    Display an overview of the DataFrame.

    Parameters:
    df: pandas DataFrame
    """
    st.write("### 🗂️ File Overview")
    st.write(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns")
    st.write(f"**Columns:** {', '.join(df.columns)}")
    st.write("### 📋 First 5 Rows of the Dataset")
    st.dataframe(df.head())
