import unittest
import pandas as pd
from unittest.mock import patch
from data_viz.utils import clean_dataframe


class TestCleanDataframe(unittest.TestCase):
    def test_column_names(self):
        """Test column name cleaning functionality."""
        data = {"First Name ": ["Alice", "Bob"], "Last  Name!": ["Smith", "Doe"]}
        df = pd.DataFrame(data)

        cleaned_df = clean_dataframe(df)

        self.assertEqual(list(cleaned_df.columns), ["first_name", "last_name"])

    @patch("streamlit.warning")
    def test_duplicate_rows(self, mock_warning):
        """Test duplicate row removal."""
        data = {"Name": ["Alice", "Bob", "Alice"], "Age": [25, 30, 25]}
        df = pd.DataFrame(data)

        cleaned_df = clean_dataframe(df)

        self.assertEqual(len(cleaned_df), 2)
        mock_warning.assert_called_once_with("Removed 1 duplicate rows")

    @patch("streamlit.info")
    def test_missing_values(self, mock_info):
        """Test missing value handling."""
        data = {"Numeric": [10, None, 30], "Categorical": ["A", None, "C"]}
        df = pd.DataFrame(data)

        cleaned_df = clean_dataframe(df)

        # Check numeric column filled with median
        self.assertEqual(cleaned_df["numeric"].isnull().sum(), 0)
        self.assertEqual(cleaned_df["numeric"].median(), 20)

        # Check categorical column filled with mode
        self.assertEqual(cleaned_df["categorical"].isnull().sum(), 0)
        self.assertEqual(set(cleaned_df["categorical"]), {"A", "C"})

        # Verify info messages called
        mock_info.assert_called()

    def test_whitespace_stripping(self):
        """Test whitespace stripping in string columns."""
        data = {
            "Name": ["  Alice  ", " Bob", "Charlie "],
            "City": [" New York ", "Chicago", " San Francisco "],
        }
        df = pd.DataFrame(data)

        cleaned_df = clean_dataframe(df)

        self.assertTrue(all(cleaned_df["name"] == ["Alice", "Bob", "Charlie"]))
        self.assertTrue(
            all(cleaned_df["city"] == ["New York", "Chicago", "San Francisco"])
        )

    @patch("streamlit.info")
    def test_categorical_column_no_mode(self, mock_info):
        """Test filling missing values in a categorical column with no mode."""
        data = {"Category": [None, None, None]}
        df = pd.DataFrame(data)

        # Print mode behavior for investigation
        print("Mode:", df["Category"].mode())
        print("Mode empty:", df["Category"].mode().empty)

        cleaned_df = clean_dataframe(df)

        # Verify the column state
        print("Cleaned column:", cleaned_df["category"].tolist())
        print("Cleaned column type:", type(cleaned_df["category"]))

        # Check column filled with empty string
        self.assertEqual(len(cleaned_df["category"]), 1)
        self.assertTrue(all(cleaned_df["category"] == ""))

        # Verify info message called
        mock_info.assert_called_once_with(
            "Filled 1 missing values in column 'category'"
        )


if __name__ == "__main__":
    unittest.main()
