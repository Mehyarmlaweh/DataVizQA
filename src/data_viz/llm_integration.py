# file: llm_integration.py
import os
import anthropic
import logging
import pandas as pd
from dotenv import load_dotenv
import base64
from io import BytesIO

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize Anthropic client
API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not API_KEY:
    raise ValueError("Anthropic API key not found in .env file.")
client = anthropic.Anthropic(api_key=API_KEY)


def call_llm_for_viz(data: pd.DataFrame, user_request: str) -> str:
    """
    Calls the LLM to generate Python visualization code based on dataset structure.
    """
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


def get_insights(image_uploaded: BytesIO) -> str:
    logger.info("Calling LLM for insights generation")

    image_data = image_uploaded.getvalue()

    if len(image_data) == 0:
        logger.error("❌ Image file is empty after reading")
        return "Error: Image file is empty"

    image_base64 = base64.b64encode(image_data).decode("utf-8")

    prompt = """
    You are a data analyst. Examine this plot and provide only key insights without any additional text or introductions.
    Guidelines:
    - The insights should be relevant to the visualization.
    - Don't Give additional text or introductions.
    - Provide only the key insights.
    - Use markdown to format the insights.
    - Each insight shoud be in a separate markdown bullet point.
    - Use markdown fomatting like Bold or italic.
    """

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
                            "media_type": "image/png",
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    )

    return response.content[0].text
