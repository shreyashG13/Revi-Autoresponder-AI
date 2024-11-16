import openai
import os
from dotenv import load_dotenv
import logging
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables
load_dotenv()

# Set OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

async def get_chatgpt_response(query: str) -> str:
    """
    Get a response from ChatGPT for a given query asynchronously.

    Args:
        query (str): The user's query.

    Returns:
        str: The response generated by ChatGPT.
    """
    try:
        logging.info(f"Sending query to ChatGPT: {query}")
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",  # Or "gpt-4"
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query}
            ],
            max_tokens=300,
            temperature=0.7,
        )
        logging.info(f"ChatGPT response: {response}")
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error interacting with ChatGPT API: {e}")
        raise e