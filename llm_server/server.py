from contextlib import asynccontextmanager

import yaml
from fastapi import FastAPI, Request
from llama_cpp import Llama
from pydantic import BaseModel


class Prompt(BaseModel):
    text: str


# create dict to hold local model after loading at app start.
models = {}


def load_local_llama(
    model_path: str,
    chat_format: str = "llama-2",
    use_mlock: bool = True,
    n_gpu_layers: int = -1,
) -> Llama:
    llm = Llama(
        model_path=model_path,
        chat_format=chat_format,
        use_mlock=use_mlock,
        n_gpu_layers=n_gpu_layers,
    )
    return llm


@asynccontextmanager
async def lifespan(app: FastAPI):
    with open("server_config.yml", "r") as server_config_file:
        # TODO: validate server config params
        server_config = yaml.safe_load(server_config_file)
        llama_config = server_config["local_llama_model"]
        llm = load_local_llama(
            model_path=llama_config["model_path"],
            chat_format=llama_config["chat_format"],
            use_mlock=llama_config["use_mlock"],
            n_gpu_layers=llama_config["n_gpu_layers"],
        )
        models["llm"] = llm
    yield
    models.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"text": "hello world"}


@app.post("/predict/")
async def predict(prompt: Prompt, max_tokens: int = 2048):
    llm_response = models["llm"](prompt=prompt.text, max_tokens=max_tokens)
    return {"llm_response": llm_response}
