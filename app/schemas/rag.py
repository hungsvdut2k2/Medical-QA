from typing import Optional

from pydantic import BaseModel, Field

__all__ = ["Document"]


class Document(BaseModel):
    title: Optional[str] = Field(
        default=None,
        title="Document Title",
        description="Document title",
    )

    description: Optional[str] = Field(
        default=None,
        title="Document Description",
        description="Document description",
    )
