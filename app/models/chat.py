import uuid
from typing import TYPE_CHECKING
from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from token_use import TokenUse
    from tool_use import ToolUse


class ChatBase(SQLModel):
    username: str = Field(default='guest', min_length=1, max_length=255, description='Username of the chat user')


class Chat(ChatBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created: datetime = Field(default_factory=datetime.now, description='Chat creation date and time')

    token_uses: list['TokenUse'] = Relationship(back_populates='chat', cascade_delete=True)
    tool_uses: list['ToolUse'] = Relationship(back_populates='chat', cascade_delete=True)


class ChatPublic(ChatBase):
    id: uuid.UUID
    created: datetime


class ChatsPublic(SQLModel):
    data: list[ChatPublic]
    count: int


class ChatCreate(ChatBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
