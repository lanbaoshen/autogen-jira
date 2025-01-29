import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from chat import Chat


class TokenUseBase(SQLModel):
    message_type: str = Field(min_length=1, max_length=255, description='What does the token used for')
    agent: str = Field(min_length=1, max_length=255, description='The name of the agent that used the token')
    prompt_tokens: int = Field(description='The tokens used for the prompt')
    completion_tokens: int = Field(description='The tokens used for the completion')


class TokenUse(TokenUseBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created: datetime = Field(default_factory=datetime.now, description='Token use date and time')
    chat_id: uuid.UUID = Field(foreign_key='chat.id', nullable=False, ondelete='CASCADE')
    chat: 'Chat' = Relationship(back_populates='token_uses')


class TokenUsePublic(TokenUseBase):
    id: uuid.UUID
    chat_id: uuid.UUID
    created: datetime


class TokenUsesPublic(SQLModel):
    data: list[TokenUsePublic]
    count: int


class TokenUseCreate(TokenUseBase):
    chat_id: uuid.UUID
