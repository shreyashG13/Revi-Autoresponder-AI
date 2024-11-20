# main.py

from fastapi import FastAPI, HTTPException
import logging
from chatgpt_handler import get_chatgpt_response
from copilot_handler import get_copilot_response
from llm_generic_handler import handle_generic_chatgpt_query, handle_generic_copilot_query
from query_handler import handle_chatgpt_query, handle_copilot_query
from ood_handler import handle_ood_query
from revi_handler import handle_revi_query  # Import the new handler

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI()

@app.get("/")
async def root():
    logging.info("Root endpoint accessed.")
    return {"message": "Revi AI Autoresponse is running!"}

@app.post("/respond/chatgpt")
async def respond_with_chatgpt(customer_id: str, query: str):
    logging.info(f"ChatGPT endpoint accessed with query: {query}")
    try:
        response = handle_chatgpt_query(customer_id, query)
        if response.get("is_ood"):
            logging.warning("Query identified as out-of-domain.")
            return {"response": handle_ood_query(query)}
        return {"response": response["response"]}
    except Exception as e:
        logging.error(f"Error in ChatGPT endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/respond/copilot")
async def respond_with_copilot(customer_id: str, query: str):
    logging.info(f"Copilot endpoint accessed with query: {query}")
    try:
        response = handle_copilot_query(customer_id, query)
        if response.get("is_ood"):
            logging.warning("Query identified as out-of-domain.")
            return {"response": handle_ood_query(query)}
        return {"response": response["response"]}
    except Exception as e:
        logging.error(f"Error in Copilot endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/respond/chatgpt/generic")
async def respond_chatgpt_generic(query: str):
    """
    Endpoint for generic ChatGPT responses.
    """
    try:
        response = handle_generic_chatgpt_query(query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/respond/copilot/generic")
async def respond_copilot_generic(query: str):
    """
    Endpoint for generic Copilot responses.
    """
    try:
        response = handle_generic_copilot_query(query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat_with_chatgpt(query: str):
    """
    Endpoint to interact with the ChatGPT API.

    Args:
        query (str): The user's query.

    Returns:
        dict: ChatGPT response.
    """
    try:
        response = await get_chatgpt_response(query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/copilot")
def chat_with_copilot(query: str):
    """
    Endpoint to interact with the Azure Copilot API.

    Args:
        query (str): The user's query.

    Returns:
        dict: Copilot response.
    """
    try:
        response = get_copilot_response(query)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# New endpoint for Revi Customer Support Assistant
@app.post("/respond/revi")
async def respond_with_revi(customer_id: str, query: str):
    logging.info(f"Revi endpoint accessed with query: {query}")
    try:
        response = await handle_revi_query(customer_id, query)
        return {"response": response}
    except Exception as e:
        logging.error(f"Error in Revi endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
