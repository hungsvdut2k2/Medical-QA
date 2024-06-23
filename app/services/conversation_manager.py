import asyncio
import json
from typing import List, Optional

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
        documents = self.vector_store.hybrid_search(search_query=message.content)
        system_prompt = self.format_prompt(documents=documents)

        if conversation[0]["role"] == "system":
            conversation[0] = {"role": "system", "content": system_prompt}
        else:
            conversation.insert(0, {"role": "system", "content": system_prompt})

        response = self.llm.response(conversation=conversation)

        self.memory.add_messages(
            message=MessageBase(conversation_id=message.conversation_id, role="assistant", content=response)
        )
        return response

    def format_prompt(self, documents: List[str]):
        base_promtpt = """
            Là một chatbot về y tế, bạn hãy dựa vào những kiến thức sau đây để trả lời câu hỏi của người dùng,
            nếu các kiến thức đó không chứa câu trả lời cho câu hỏi của người dùng hãy tự đưa ra câu trả lời
            không dựa vào các tài liệu.
            1. {first_document}
            2. {second_document}
            """.format(
            first_document=documents[0], second_document=documents[1]
        )

        return base_promtpt
