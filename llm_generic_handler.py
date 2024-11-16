import openai
import requests
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables
load_dotenv()

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Azure OpenAI Endpoint and Key (for Copilot)
AZURE_COPILOT_ENDPOINT = os.getenv("AZURE_COPILOT_ENDPOINT")
AZURE_COPILOT_KEY = os.getenv("AZURE_COPILOT_KEY")

def handle_generic_chatgpt_query(query: str) -> str:
    """
    Handles generic chatbot queries using ChatGPT.
    """
    try:
        logging.info("Sending generic query to ChatGPT.")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for general queries."},
                {"role": "user", "content": query},
            ],
            max_tokens=400,
            temperature=0.7,
        )
        logging.info(f"ChatGPT generic response: {response}")
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        logging.error(f"Error in ChatGPT generic query: {e}")
        return "I'm sorry, I couldn't process your request."

def handle_generic_copilot_query(query: str) -> str:
    """
    Handles generic chatbot queries using Azure Copilot.
    """
    try:
        logging.info("Sending generic query to Azure Copilot.")
        headers = {"Content-Type": "application/json", "api-key": AZURE_COPILOT_KEY}
        payload = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant for general queries."},
                {"role": "user", "content": query},
            ],
            "max_tokens": 400,
            "temperature": 0.7,
        }
        response = requests.post(f"{AZURE_COPILOT_ENDPOINT}/chat/completions", headers=headers, json=payload)
        logging.info(f"Copilot generic response: {response.json()}")
        response_data = response.json()

        if response.status_code == 200:
            return response_data["choices"][0]["message"]["content"]
        else:
            return f"Error: {response_data.get('error', {}).get('message', 'Unknown error')}"
    except Exception as e:
        logging.error(f"Error in Copilot generic query: {e}")
        return "I'm sorry, I couldn't process your request."
