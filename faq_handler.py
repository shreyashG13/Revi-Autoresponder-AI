from faq_loader import load_faq, find_similar_faq
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

FAQS = load_faq()

def handle_faq_query(query: str) -> dict:
    """
    Handles domain-specific FAQ queries by finding similar FAQs.
    """
    similar_faq = find_similar_faq(query, FAQS)
    if similar_faq:
        logging.info(f"FAQ match found for query: {similar_faq}")
        return {"response": similar_faq["answer"], "origin": "FAQ"}
    else:
        logging.warning("No FAQ match found.")
        return {"response": "I'm sorry, I couldn't find an answer in the FAQ.", "origin": "FAQ"}
