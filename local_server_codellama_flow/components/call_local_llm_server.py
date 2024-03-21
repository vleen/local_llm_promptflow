import json
import requests
from promptflow import tool


@tool
def call_local_llama(user_input: str, llm_endpoint: str, max_tokens: int = 2048) -> str:

    try:
        llm_response = requests.post(
            llm_endpoint,
            data=json.dumps({"text": user_input, "max_tokens": max_tokens}),
        )
        llm_response.raise_for_status()  # Raise an exception for non-2xx status codes
        llm_response_json = llm_response.json()
        return llm_response_json
    except requests.RequestException as e:
        # Handle request-related exceptions
        raise ValueError(f"Error occurred during LLM request: {e}")
    except json.JSONDecodeError as e:
        # Handle JSON decoding error
        raise ValueError(f"Error occurred during JSON decoding: {e}")
