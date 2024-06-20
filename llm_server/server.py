from contextlib import asynccontextmanager

import yaml
from fastapi import FastAPI, Request
from llama_cpp import Llama
from pydantic import BaseModel


class Prompt(BaseModel):
    text: str


# create dict to hold local model after loading at app start.
models = {}


def load_local_llama(config_file_path: str = "server_config.yml") -> Llama:
    try:
        with open(config_file_path, "r") as server_config_file:
            server_config = yaml.safe_load(server_config_file)
            if not isinstance(server_config, dict):
                raise ValueError("Invalid YAML file format")

            if "local_llama_model" not in server_config:
                raise KeyError("Key 'local_llama_model' not found in the YAML file")

            llama_config = server_config["local_llama_model"]
            return Llama(**llama_config)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Config file '{config_file_path}' not found") from e
    except yaml.YAMLError as e:
        raise ValueError(f"Error loading YAML file: {e}") from e


@asynccontextmanager
async def lifespan(app: FastAPI):

    llm = load_local_llama()
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
