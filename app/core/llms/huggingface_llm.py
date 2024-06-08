from typing import Any, Dict, List, Optional

from ctransformers import AutoModelForCausalLM
from transformers import AutoTokenizer

from app.schemas import InferenceParams, InitParams


class HuggingFaceLLM:
    def __init__(self, int_parameters: Optional[InitParams], inference_parameters: Optional[InferenceParams]):
        self.model = AutoModelForCausalLM.from_pretrained(**int_parameters.model_dump())
        self.tokenizer = AutoTokenizer.from_pretrained(int_parameters.model_path_or_repo_id)
        self.inference_parameters = inference_parameters

    def response(self, conversation: List[Dict[str, Any]]):
        input_message = self.tokenizer.apply_chat_template(conversation, tokenize=False)
        response = self.model(input_message, **self.inference_parameters.model_dump())
        return response
