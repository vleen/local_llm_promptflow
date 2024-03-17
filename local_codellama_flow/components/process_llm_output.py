from promptflow import tool


@tool
def process_llm_output(llm_output: str) -> str:
    llm_output_processed = llm_output["choices"][0]["text"]

    return llm_output_processed
