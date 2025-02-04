from data_viz.home import main
import unittest
from unittest.mock import patch, MagicMock, ANY
import pandas as pd
import streamlit as st
from io import StringIO
import data_viz.home
import importlib


class TestHome(unittest.TestCase):
    @patch("data_viz.home.st.file_uploader")
    @patch("data_viz.home.read_uploaded_file")
    @patch("data_viz.home.clean_dataframe")
    @patch("data_viz.home.display_dataframe_overview")
    @patch("data_viz.home.st.button")
    @patch("data_viz.home.st.columns")
    @patch("data_viz.home.st.toggle")
    @patch("data_viz.home.st.success")
    @patch("data_viz.home.st.info")
    def test_file_upload_and_cleaning_show_cleaned(
        self,
        mock_info,
        mock_success,
        mock_toggle,
        mock_columns,
        mock_button,
        mock_display,
        mock_clean,
        mock_read,
        mock_uploader,
    ):
        def columns_side_effect(n):
            if isinstance(n, list):
                num_cols = len(n)
            else:
                num_cols = n
            cols = [MagicMock() for _ in range(num_cols)]
            for col in cols:
                col.__enter__ = MagicMock(return_value=col)
                col.__exit__ = MagicMock(return_value=None)
            return cols

        mock_columns.side_effect = columns_side_effect
        mock_uploader.return_value = MagicMock(name="uploaded_file")
        test_df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
        cleaned_df = pd.DataFrame({"A": [1, 2], "B": [3, 4], "C": [5, 6]})

        mock_read.return_value = test_df
        mock_clean.return_value = cleaned_df
        mock_button.return_value = True
        mock_toggle.return_value = True

        session_state_mock = MagicMock()
        session_state_mock.raw_df = test_df
        session_state_mock.cleaned_df = cleaned_df

        with patch("streamlit.session_state", session_state_mock):
            main()

        mock_display.assert_called_with(cleaned_df)
        mock_info.assert_called_with("Showing cleaned data")

    @patch("data_viz.home.st.file_uploader")
    @patch("data_viz.home.read_uploaded_file")
    @patch("data_viz.home.clean_dataframe")
    @patch("data_viz.home.display_dataframe_overview")
    @patch("data_viz.home.st.button")
    @patch("data_viz.home.st.columns")
    @patch("data_viz.home.st.toggle")
    @patch("data_viz.home.st.success")
    @patch("data_viz.home.st.info")
    def test_file_upload_and_cleaning_show_raw(
        self,
        mock_info,
        mock_success,
        mock_toggle,
        mock_columns,
        mock_button,
        mock_display,
        mock_clean,
        mock_read,
        mock_uploader,
    ):
        def columns_side_effect(n):
            if isinstance(n, list):
                num_cols = len(n)
            else:
                num_cols = n
            cols = [MagicMock() for _ in range(num_cols)]
            for col in cols:
                col.__enter__ = MagicMock(return_value=col)
                col.__exit__ = MagicMock(return_value=None)
            return cols

        mock_columns.side_effect = columns_side_effect
        mock_uploader.return_value = MagicMock(name="uploaded_file")
        test_df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
        cleaned_df = pd.DataFrame({"A": [1, 2], "B": [3, 4], "C": [5, 6]})

        mock_read.return_value = test_df
        mock_clean.return_value = cleaned_df
        mock_button.return_value = True
        mock_toggle.return_value = False  # Show raw data

        session_state_mock = MagicMock()
        session_state_mock.raw_df = test_df
        session_state_mock.cleaned_df = cleaned_df

        with patch("streamlit.session_state", session_state_mock):
            main()

        mock_display.assert_called_with(test_df)
        mock_info.assert_called_with("Showing raw data")

    @patch("data_viz.home.st.markdown")
    @patch("data_viz.home.st.title")
    def test_page_layout(self, mock_title, mock_markdown):
        main()
        mock_title.assert_called_once_with("📊 Data Viz QA")
        self.assertTrue(mock_markdown.called)
        markdown_calls = [call[0][0] for call in mock_markdown.call_args_list]
        self.assertTrue(
            any(
                "### Empower Your Data" in call
                for call in markdown_calls
                if isinstance(call, str)
            )
        )


comment='''
    def test_main_execution(self):
        with patch("data_viz.home.main") as mock_main:
            # Execute the __main__ block directly
            exec(
                compile(
                    """
if True:  # Simulate __name__ == "__main__"
    main()
""",
                    "",
                    "exec",
                ),
                {"main": mock_main},
            )
            mock_main.assert_called_once_with()
'''

if __name__ == "__main__":
    unittest.main()
