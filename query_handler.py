import openai
import requests
import os
import logging
from dotenv import load_dotenv
from faq_loader import load_faq, find_similar_faq

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

load_dotenv()

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


# Azure OpenAI Endpoint and Key (for Copilot)
AZURE_COPILOT_ENDPOINT = os.getenv("AZURE_COPILOT_ENDPOINT")
AZURE_COPILOT_KEY = os.getenv("AZURE_COPILOT_KEY")

# Load FAQs for matching
FAQS = load_faq()

def handle_chatgpt_query(customer_id: str, query: str) -> dict:
    """Handles queries using ChatGPT (OpenAI API)."""
    logging.info(f"ChatGPT query received for customer {customer_id}: {query}")
    similar_faq = find_similar_faq(query, FAQS)
    if similar_faq:
        logging.info(f"FAQ match found for query: {similar_faq}")
        return {"response": similar_faq["answer"], "origin": "FAQ", "is_ood": False}

    try:
        logging.info("Sending query to ChatGPT API.")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful fitness assistant for gym-related queries."},
                {"role": "user", "content": query},
            ],
            max_tokens=400,
            temperature=0.7,
        )
        logging.info(f"ChatGPT response: {response}")
        return {"response": response["choices"][0]["message"]["content"], "origin": "ChatGPT", "is_ood": False}
    except openai.error.APIError as api_err:
        logging.error(f"ChatGPT APIError: {api_err}")
        return {"response": f"API Error: {api_err}", "origin": "ChatGPT", "is_ood": True}
    except openai.error.InvalidRequestError as invalid_req_err:
        logging.error(f"ChatGPT InvalidRequestError: {invalid_req_err}")
        return {"response": f"Invalid Request: {invalid_req_err}", "origin": "ChatGPT", "is_ood": True}
    except Exception as e:
        logging.error(f"Unexpected error with ChatGPT: {e}")
        return {"response": f"Unexpected error: {e}", "origin": "ChatGPT", "is_ood": True}

def handle_copilot_query(customer_id: str, query: str) -> dict:
    """Handles queries using Copilot (Azure OpenAI Service)."""
    logging.info(f"Copilot query received for customer {customer_id}: {query}")
    similar_faq = find_similar_faq(query, FAQS)
    if similar_faq:
        logging.info(f"FAQ match found for query: {similar_faq}")
        return {"response": similar_faq["answer"], "origin": "FAQ", "is_ood": False}

    try:
        logging.info("Sending query to Azure Copilot API.")
        headers = {"Content-Type": "application/json", "api-key": AZURE_COPILOT_KEY}
        payload = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "You are a helpful fitness assistant for gym-related queries."},
                {"role": "user", "content": query},
            ],
            "max_tokens": 400,
            "temperature": 0.7,
        }
        response = requests.post(f"{AZURE_COPILOT_ENDPOINT}/chat/completions", headers=headers, json=payload)
        logging.info(f"Copilot response: {response.json()}")
        response_data = response.json()

        if response.status_code == 200:
            return {"response": response_data["choices"][0]["message"]["content"], "origin": "Copilot", "is_ood": False}
        else:
            logging.warning(f"Copilot returned an error: {response_data}")
            return {"response": response_data.get("error", {}).get("message", "Unknown error"), "origin": "Copilot", "is_ood": True}
    except requests.RequestException as e:
        logging.error(f"Error while connecting to Copilot: {e}")
        return {"response": f"Request Error: {e}", "origin": "Copilot", "is_ood": True}
