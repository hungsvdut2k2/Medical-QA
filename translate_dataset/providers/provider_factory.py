from typing import Optional

from .base_provider import BaseProvider
from .conversation_provider import ConversationProvider
from .instruction_provider import InstructionProvider
from .question_answer_provider import QuestionAnswerProvider


class ProviderFactory:
    def __init__(self):
        self.providers = {
            "question_answer": QuestionAnswerProvider,
            "instruction": InstructionProvider,
            "conversation": ConversationProvider,
        }

    def get_provider(self, provider_name: Optional[str], **kwargs) -> Optional[BaseProvider]:
        return self.providers[provider_name](**kwargs)
