from typing import Optional

from pydantic import BaseModel, Field

__all__ = ["MessageBase"]


class MessageBase(BaseModel):
    conversation_id: Optional[str] = Field(default=None, title="Conversation ID", description="Conversation ID")
    role: Optional[str] = Field(default=None, title="Role", description="Role")
    content: Optional[str] = Field(default=None, title="Content", description="Content")
