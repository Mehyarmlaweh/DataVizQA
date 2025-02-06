import unittest
from unittest.mock import patch, MagicMock
from io import BytesIO
from data_viz.llm_integration import get_insights


class TestGetInsights(unittest.TestCase):
    def setUp(self):
        self.mock_image = BytesIO(b"fake image data")
        self.empty_image = BytesIO(b"")

    def test_empty_image_error(self):
        result = get_insights(self.empty_image)
        self.assertIn("Error: Image file is empty", result)


if __name__ == "__main__":
    unittest.main()
