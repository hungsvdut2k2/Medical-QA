import os

import yaml
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    CONFIG_FILE_PATH: str = os.getenv("CONFIG_FILE_PATH")


settings = Settings()
config = yaml.safe_load(open(settings.CONFIG_FILE_PATH))


class AppSettings(BaseSettings):
    model_path_or_repo_id: str = config["LLM"]["model_path_or_repo_id"]
    model_file: str = config["LLM"]["model_file"]
    model_type: str = config["LLM"]["model_type"]
    context_length: int = config["LLM"]["context_length"]
    gpu_layers: int = config["LLM"]["gpu_layers"]
    top_k: int = config["LLM"]["top_k"]
    top_p: float = config["LLM"]["top_p"]
    temperature: float = config["LLM"]["temperature"]
    stream: bool = config["LLM"]["stream"]

    memory_top_k: int = config["Memory"]["top_k"]

    host_url: str = config["VectorStore"]["host_url"]
    model_name: str = config["VectorStore"]["model_name"]
    collection: str = config["VectorStore"]["collection"]


app_settings = AppSettings()
