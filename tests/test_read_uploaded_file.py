import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from data_viz.utils import read_uploaded_file


class TestReadUploadedFile(unittest.TestCase):
    """
    Tests for the `read_uploaded_file` function, which handles reading
    CSV and Excel files into a pandas DataFrame.
    """

    @patch("pandas.read_csv")
    def test_read_csv(self, mock_read_csv):
        """
        Test case for reading a CSV file.
        Mocks a CSV file upload and checks if the file is correctly read into a DataFrame.
        """
        # Mock the CSV reading process
        mock_file = MagicMock()
        mock_file.name = "test_file.csv"
        mock_file.read.return_value = b"A,B\n1,2\n3,4"  # Mock file content

        # Mock `pandas.read_csv` to return a DataFrame
        mock_read_csv.return_value = pd.DataFrame({"A": [1, 3], "B": [2, 4]})

        # Call the function with the mocked file
        df = read_uploaded_file(mock_file)
        
        # Assertions to verify correct behavior
        self.assertEqual(df.shape, (2, 2))  # Should have 2 rows and 2 columns
        mock_read_csv.assert_called_once_with(mock_file)  # Ensure read_csv was called with the mock file

    @patch("pandas.read_excel")
    def test_read_excel(self, mock_read_excel):
        """
        Test case for reading an Excel file.
        Mocks an Excel file upload and checks if the file is correctly read into a DataFrame.
        """
        mock_file = MagicMock()
        mock_file.name = "test_file.xlsx"
        mock_file.read.return_value = b"excel_content"  # Just for testing, no actual content parsing here

        # Mock `pandas.read_excel` to return a DataFrame
        mock_read_excel.return_value = pd.DataFrame({"A": [1, 2], "B": [3, 4]})

        # Call the function with the mocked file
        df = read_uploaded_file(mock_file)

        # Assertions to verify correct behavior
        self.assertEqual(df.shape, (2, 2))  # Should have 2 rows and 2 columns
        mock_read_excel.assert_called_once_with(mock_file)  # Ensure read_excel was called with the mock file

    def test_invalid_file_format(self):
        """
        Test case for handling an unsupported file format.
        Checks that the function returns None when an unsupported file type is uploaded.
        """
        mock_file = MagicMock()
        mock_file.name = "test_file.txt"
        result = read_uploaded_file(mock_file)
        self.assertIsNone(result)  # Should return None for unsupported format
    
    @patch('streamlit.error')
    @patch('pandas.read_csv')
    def test_read_csv_error(self, mock_read_csv, mock_st_error):
        """
        Test error handling when reading CSV fails.
        """
        # Simulate an exception during file reading
        mock_read_csv.side_effect = Exception("Corrupted file")
        
        mock_file = MagicMock()
        mock_file.name = "test_file.csv"
        
        # Call the function
        result = read_uploaded_file(mock_file)
        
        # Verify error handling
        self.assertIsNone(result)
        mock_st_error.assert_called_once_with("Error reading file: Corrupted file")
        mock_read_csv.assert_called_once_with(mock_file)

    @patch('streamlit.error')
    @patch('pandas.read_excel')
    def test_read_excel_error(self, mock_read_excel, mock_st_error):
        """
        Test error handling when reading Excel fails.
        """
        # Simulate an exception during file reading
        mock_read_excel.side_effect = Exception("Corrupted Excel file")
        
        mock_file = MagicMock()
        mock_file.name = "test_file.xlsx"
        
        # Call the function
        result = read_uploaded_file(mock_file)
        
        # Verify error handling
        self.assertIsNone(result)
        mock_st_error.assert_called_once_with("Error reading file: Corrupted Excel file")
        mock_read_excel.assert_called_once_with(mock_file)

if __name__ == "__main__":
    unittest.main()