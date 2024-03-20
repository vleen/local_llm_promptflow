import json

import requests
from llama_cpp import Llama
from promptflow import tool


@tool
def call_local_llama(user_input: str, llm_endpoint: str, max_tokens: int = 2048) -> str:
    # llm_response = llm(prompt=prompt, max_tokens=max_tokens, echo=False)
    llm_response = requests.post(
        llm_endpoint, data=json.dumps({"text": user_input, "max_tokens": max_tokens})
    ).json()

    return llm_response
