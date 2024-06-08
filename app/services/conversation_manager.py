from typing import Optional

from app.core.llms import HuggingFaceLLM
from app.core.memories import ConversationMemory
from app.core.vector_stores import QdrantVectorStore
from app.schemas import MessageBase


class ConversationManager:
    def __init__(
        self,
        llm: Optional[HuggingFaceLLM],
        memory: Optional[ConversationMemory],
        vector_store: Optional[QdrantVectorStore],
    ):
        self.llm = llm
        self.memory = memory
        self.vector_store = vector_store

    def handle_conversation(self, message: MessageBase):
        self.memory.add_messages(message=message)
        conversation = self.memory.get_conversation(message.conversation_id)
        response = self.llm.response(conversation=conversation)
        self.memory.add_messages(
            message=MessageBase(conversation_id=message.conversation_id, role="assistant", content=response)
        )
        return response
