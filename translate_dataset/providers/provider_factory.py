from typing import Optional
from .base_provider import BaseProvider
from .question_answer_provider import QuestionAnswerProvider

class ProviderFactory:
    def __init__(self):
        self.providers = {
            "question_answer": QuestionAnswerProvider
        }

    def get_provider(self, provider_name: Optional[str], **kwargs) -> BaseProvider:
        return self.providers[provider_name](**kwargs)