import streamlit as st
import pandas as pd


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
    df_cleaned.columns = df_cleaned.columns.str.replace(r"\s+", "_", regex=True)
    df_cleaned.columns = df_cleaned.columns.str.replace(r"[^\w\s]", "", regex=True)

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
                if not df_cleaned[column].mode().empty:
                    df_cleaned[column] = df_cleaned[column].fillna(
                        df_cleaned[column].mode()[0]
                    )
                else:
                    df_cleaned[column] = df_cleaned[column].fillna("")
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
