from typing import Any, Dict, List, Optional

from app.schemas import MessageBase


class ConversationMemory:
    def __init__(self, top_k: Optional[int]):
        self.memory = {}
        self.top_k = top_k

    def add_messages(self, message: MessageBase):
        if message.conversation_id in self.memory:
            self.memory[message.conversation_id].append(message)

            if len(self.memory[message.conversation_id]) > self.top_k:
                self.memory[message.conversation_id].pop(0)

        else:
            self.memory[message.conversation_id] = [{"role": message.role, "content": message.content}]

    def get_conversation(self, conversation_id: Optional[str]) -> List[Dict[str, Any]]:
        if conversation_id in self.memory:
            return self.memory[conversation_id]

        return []

    def clear_conversation(self, conversation_id: Optional[str]):
        if conversation_id in self.memory:
            self.memory.pop(conversation_id)
