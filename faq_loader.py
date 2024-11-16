from typing import List, Dict
from difflib import SequenceMatcher

def load_faq() -> List[Dict[str, str]]:
    """
    Load FAQs for retrieval-augmented generation (RAG) or domain-specific response.

    Returns:
        List[Dict[str, str]]: A list of FAQs with questions and answers.
    """
    return [
        {"question": "What are the gym hours?", "answer": "6 AM to 10 PM daily."},
        {"question": "Are trainers available?", "answer": "Trainers are available from 8 AM to 8 PM."},
        {"question": "How do I book a session?", "answer": "Use the app to book a session or contact the front desk."},
        {"question": "What membership plans do you offer?", "answer": "We offer monthly, quarterly, and annual plans."},
        {"question": "Do you provide diet plans?", "answer": "Yes, you can consult our trainers for personalized diet plans."},
        {"question": "Can I freeze my membership?", "answer": "Yes, memberships can be frozen for up to 3 months."},
        {"question": "What is the cancellation policy?", "answer": "You can cancel anytime, but fees are non-refundable."},
        {"question": "Do you have group classes?", "answer": "Yes, we offer yoga, pilates, and strength training classes."},
        {"question": "What is the trainer fee?", "answer": "Trainer fees start from $50 per session."},
        {"question": "Are there discounts for students?", "answer": "Yes, we offer a 20% discount for students with valid ID."},
    ]

def find_similar_faq(query: str, faqs: List[Dict[str, str]], similarity_threshold: float = 0.7) -> Dict[str, str]:
    """
    Find a similar FAQ based on the similarity between the query and stored FAQ questions.

    Args:
        query (str): The user's query.
        faqs (List[Dict[str, str]]): A list of FAQs.
        similarity_threshold (float): Minimum similarity threshold to match a question.

    Returns:
        Dict[str, str]: The matched FAQ or None if no similar FAQ is found.
    """
    for faq in faqs:
        similarity = SequenceMatcher(None, query.lower(), faq["question"].lower()).ratio()
        if similarity >= similarity_threshold:
            return faq
    return None
