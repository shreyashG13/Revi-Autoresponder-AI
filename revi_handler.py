# revi_handler.py

import os
from dotenv import load_dotenv
import openai
import logging
import json

# Load environment variables
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Set the path to the project root directory
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Set the path to the utils directory
UTILS_DIR = os.path.join(PROJECT_ROOT, 'utils')

# Function to load the system prompt from file
def load_system_prompt():
    prompt_path = os.path.join(UTILS_DIR, 'system_prompt.txt')
    with open(prompt_path, 'r', encoding='utf-8') as file:
        system_prompt = file.read()
    return system_prompt

# Function to load FAQs from JSON file
def load_faqs():
    faqs_path = os.path.join(UTILS_DIR, 'faqs.json')
    with open(faqs_path, 'r', encoding='utf-8') as file:
        faqs = json.load(file)
    return faqs

async def handle_revi_query(customer_id: str, query: str):
    try:
        # Load the system prompt
        SYSTEM_PROMPT = load_system_prompt()
        
        # Optionally, load FAQs if needed for additional processing
        # faqs = load_faqs()  # Uncomment if you need to use FAQs
        
        # Prepare the messages for the ChatCompletion
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query}
        ]
    
        # Make the API call to OpenAI
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",  # Use "gpt-4" if you have access
            messages=messages,
            temperature=0.7,  # Adjust as needed
            max_tokens=500,   # Adjust as needed
            stop=None
        )
    
        # Extract the assistant's reply
        assistant_reply = response['choices'][0]['message']['content'].strip()
    
        # Log the interaction
        logging.info(f"Assistant response: {assistant_reply}")
    
        return assistant_reply
    
    except Exception as e:
        logging.error(f"Error in handle_revi_query: {e}")
        raise e
