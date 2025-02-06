import os
import anthropic
import logging
import pandas as pd
from dotenv import load_dotenv
import base64
from typing import Union
from io import BytesIO

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize Anthropic client
#API_KEY = os.getenv("ANTHROPIC_API_KEY")
#if not API_KEY:
#    raise ValueError("Anthropic API key not found in .env file.")
#client = anthropic.Anthropic(api_key=API_KEY)


def call_llm_for_viz(data: pd.DataFrame, user_request: str,API_KEY:str) -> str:
    """
    Calls the LLM to generate Python visualization code based on dataset structure.
    """
    client = anthropic.Anthropic(api_key=API_KEY)

    if data.empty:
        logger.error("❌ Empty DataFrame provided for visualization")
        return "Error: Empty DataFrame provided"
    else:
        dataset_info = f"""
        Column Names and Types:
        {data.dtypes.to_string()}

        Dataset Description:
        {data.describe(include='all').to_string()}
        """

        llm_prompt = f"""
        You are an expert in Python data visualization. Given the dataset structure below, generate an optimal visualization 
        using either `matplotlib`, `seaborn`, or `plotly` based on the user request.

        Dataset Overview:
        {dataset_info}

        User Request:
        {user_request}

        Guidelines:
        - Use only Python code, with no explanations or comments.
        - Ensure the code is executable within a Streamlit app.
        - Use the exact column names from the dataset.
        - The visualization should be relevant to the dataset's structure.
        - If necessary, infer numerical, categorical, or time-based trends.
        - Use directly the df variable in the environment to access the dataset. don't redefine it.

        Provide **only** the Python code output.
        """

        logger.info("Calling LLM for visualization generation")

        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=8000,
            messages=[{"role": "user", "content": llm_prompt}],
        )

        return response.content[0].text


def get_insights(image_uploaded: Union[bytes, "BytesIO"], API_KEY: str) -> str:
    """
    Analyze an uploaded image using LLM to generate insights about the visualization.
    
    Args:
        image_uploaded (Union[bytes, BytesIO]): The uploaded image file in bytes or BytesIO format.
        API_KEY (str): The API key for the Anthropic service.
    
    Returns:
        str: Markdown-formatted string containing key insights about the visualization.
             Returns an error message if the image processing fails.
    
    Raises:
        None: Errors are logged and returned as strings in the response.
    """
    try:
        # Initialize the Anthropic client
        client = anthropic.Anthropic(api_key=API_KEY)
        logger.info("Calling LLM for insights generation")

        # Convert the image to bytes if it's in BytesIO format
        if hasattr(image_uploaded, "getvalue"):
            image_data = image_uploaded.getvalue()
        else:
            image_data = image_uploaded

        if len(image_data) == 0:
            logger.error("❌ Image file is empty after reading")
            return "Error: Image file is empty"

        # Encode the image data to Base64
        image_base64 = base64.b64encode(image_data).decode("utf-8")

        # Determine the media type (PNG or JPEG) based on the file content
        media_type = "image/png" if image_data.startswith(b"\x89PNG") else "image/jpeg"

        # Define the prompt for Claude
        prompt = """
        You are a data analyst. Examine this plot and provide only key insights without any additional text or introductions.
        Guidelines:
        - The insights should be relevant to the visualization.
        - Don't give additional text or introductions.
        - Provide only the key insights.
        - Use markdown to format the insights.
        - Each insight should be in a separate markdown bullet point.
        - Use markdown formatting like **bold** or *italic*.
        """

        # Send the request to Claude with the image and prompt
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "data": image_base64,
                                "media_type": media_type,  
                            },
                        },
                        {"type": "text", "text": prompt},
                    ],
                }
            ],
        )

        # Extract and return the generated insights
        return response.content[0].text

    except Exception as e:
        logger.error(f"❌ Error generating insights: {e}")
        return f"Error: {str(e)}"