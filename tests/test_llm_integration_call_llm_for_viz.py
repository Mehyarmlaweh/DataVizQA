import unittest
import pandas as pd
from unittest.mock import patch, MagicMock
from data_viz.llm_integration import call_llm_for_viz

class TestCallLLMForViz(unittest.TestCase):
    def setUp(self):
        self.sample_df = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': ['a', 'b', 'c']
        })


    @patch('anthropic.Anthropic')
    def test_llm_call_with_empty_df(self, mock_client):
        empty_df = pd.DataFrame()
        result = call_llm_for_viz(empty_df, "Create a plot")
        
        self.assertEqual(result, "Error: Empty DataFrame provided")
        mock_client.return_value.messages.create.assert_not_called()

if __name__ == '__main__':
    unittest.main()
