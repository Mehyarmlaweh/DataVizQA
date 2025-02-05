import unittest
import pandas as pd
from unittest.mock import patch
from data_viz.utils import display_dataframe_overview

class TestDisplayDataframeOverview(unittest.TestCase):
    @patch('streamlit.write')
    @patch('streamlit.dataframe')
    def test_overview_display(self, mock_dataframe, mock_write):
        """Test DataFrame overview display."""
        data = {
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [25, 30, 35],
            'City': ['New York', 'Chicago', 'San Francisco']
        }
        df = pd.DataFrame(data)
        
        # Call the function
        display_dataframe_overview(df)
        
        # Verify write calls
        write_calls = [call[0][0] for call in mock_write.call_args_list]
        
        # Check for file overview header
        self.assertTrue(any("🗂️ File Overview" in str(call) for call in write_calls))
        
        # Check for shape and columns information
        self.assertTrue(any("3 rows × 3 columns" in str(call) for call in write_calls))
        self.assertTrue(any("Name, Age, City" in str(call) for call in write_calls))
        
        # Verify dataframe display
        mock_dataframe.assert_called_once()

if __name__ == '__main__':
    unittest.main()