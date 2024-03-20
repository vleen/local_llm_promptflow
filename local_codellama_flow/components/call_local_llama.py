from llama_cpp import Llama
from promptflow import tool


@tool
def call_local_llama(prompt: str, llm: Llama, max_tokens: int = 2048) -> str:
    llm_response = llm(prompt=prompt, max_tokens=max_tokens, echo=False)
    return llm_response
