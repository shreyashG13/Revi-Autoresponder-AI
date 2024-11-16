# Revi-Autoresponder-AI

Revi-Autoresponder-AI is an intelligent autoresponder project designed to handle customer queries efficiently using integration with OpenAI's ChatGPT and Azure Copilot. The project utilizes FastAPI for the backend, allowing seamless integration with Large Language Models (LLMs) for both general and domain-specific queries.

---

## Features

- **ChatGPT Integration**: Leverages OpenAI's API for natural language query responses.
- **Azure Copilot Integration**: Provides additional response capabilities for customer interactions.
- **Domain-Specific Queries**: Handles fitness and gym-related FAQs, such as workout plans, trainer availability, and more.
- **Out-of-Domain (OOD) Handling**: Gracefully identifies and manages queries that are beyond the chatbot's domain.
- **Swagger Documentation**: Interactive API documentation available at `/docs`.

---

## Endpoints

The application provides the following endpoints:

### ChatGPT Integration
- **POST /chat**
  - **Description**: Handles queries via OpenAI's ChatGPT API.
  - **Request**:
    ```json
    {
      "query": "Can you suggest a 7-day gym workout plan?"
    }
    ```
  - **Response**:
    ```json
    {
      "response": "Day 1: Chest & Triceps, Day 2: Back & Biceps, etc."
    }
    ```

### Copilot Integration
- **POST /copilot**
  - **Description**: Handles queries via Azure Copilot API.
  - **Request**:
    ```json
    {
      "query": "Can you suggest a good diet plan?"
    }
    ```
  - **Response**:
    ```json
    {
      "response": "Focus on protein-rich foods and avoid sugar."
    }
    ```

### FAQ Management
- **GET /faq**
  - **Description**: Fetches all available FAQs for domain-specific responses.
  - **Response**:
    ```json
    [
      {
        "question": "What are the gym hours?",
        "answer": "6 AM to 10 PM daily."
      },
      {
        "question": "Are trainers available?",
        "answer": "Trainers are available from 8 AM to 8 PM."
      }
    ]
    ```

---

## How to Run

### Requirements
- Python 3.8+
- `pipenv` or `venv`
- OpenAI and Azure Copilot API keys

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/shreyashG13/Revi-Autoresponder-AI.git
   cd Revi-Autoresponder-AI
