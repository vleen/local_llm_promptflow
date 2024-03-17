from llama_cpp import Llama
from promptflow import tool


@tool
def load_local_llama(
    model_filename: str,
    model_path: str = "./",
    chat_format: str = "llama-2",
    use_mlock: bool = True,
    n_gpu_layers: int = -1,
) -> Llama:
    llm = Llama(
        model_path=model_path + model_filename,
        chat_format=chat_format,
        use_mlock=use_mlock,
        n_gpu_layers=n_gpu_layers,
    )

    return llm
