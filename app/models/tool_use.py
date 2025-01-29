import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from chat import Chat


class ToolUseBase(SQLModel):
    tool_name: str = Field(min_length=1, max_length=255, description='The name of the tool used')
    agent: str = Field(min_length=1, max_length=255, description='The name of the agent that used the tool')
    result: bool = Field(description='The result of the tool use')


class ToolUse(ToolUseBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created: datetime = Field(default_factory=datetime.now, description='Tool use date and time')
    chat_id: uuid.UUID = Field(foreign_key='chat.id', nullable=False, ondelete='CASCADE')
    chat: 'Chat' = Relationship(back_populates='tool_uses')


class ToolUsePublic(ToolUseBase):
    id: uuid.UUID
    chat_id: uuid.UUID
    created: datetime


class ToolUsesPublic(SQLModel):
    data: list[ToolUsePublic]
    count: int


class ToolUseCreate(ToolUseBase):
    chat_id: uuid.UUID
