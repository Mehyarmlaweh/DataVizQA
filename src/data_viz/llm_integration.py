# file: llm_integration.py
import os
import anthropic
import logging
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
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

    Provide **only** the Python code output.
    """
    
    logger.info("Calling LLM for visualization generation")
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=8000,
        messages=[{"role": "user", "content": llm_prompt}]
    )
    
    return response.content[0].text
