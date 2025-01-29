import uuid
from typing import Literal
from datetime import datetime

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from jinja2 import Template
from sqlmodel import func, select

from app.api.deps import SessionDep
from app.core.config import settings
from app.models import ChatsPublic, Chat, TokenUsesPublic, TokenUse, ToolUsesPublic, ToolUse
from app.utils.template import load_template

router = APIRouter(prefix='/meas', tags=['meas'])


meas_html = load_template('meas.html')

@router.get('/')
async def get():
    html = Template(meas_html).render(
        model=settings.AZURE_MODEL if settings.MODEL_CLIENT == 'azure' else settings.OPENAI_MODEL,
        token_use_url=f'{settings.server_host}{router.prefix}/token-uses',
        chat_url=f'{settings.server_host}{router.prefix}/chats',
        tool_use_url=f'{settings.server_host}{router.prefix}/tool-uses',
    )
    return HTMLResponse(html)


@router.get('/chats', response_model=ChatsPublic)
def get_chats(
        session: SessionDep,
        id: uuid.UUID = None,
        started: datetime = None,
        ended: datetime = None,
        offset: int = 0,
        limit: int = 100
):
    where = [
        Chat.id == id if id else None,
        Chat.created >= started if started else None,
        Chat.created <= ended if ended else None
    ]
    where = [condition for condition in where if condition is not None]

    count_statement = select(func.count()).select_from(Chat).where(*where)
    count = session.exec(count_statement).one()

    statement = select(Chat).select_from(Chat).where(*where).offset(offset).limit(limit)
    chats = session.exec(statement).all()

    return ChatsPublic(data=chats, count=count)


@router.get('/token-uses', response_model=TokenUsesPublic)
def get_token_uses(
        session: SessionDep,
        id: uuid.UUID = None,
        chat_id: uuid.UUID = None,
        message_type: Literal['ToolCallRequestEvent', 'TextMessage'] = None,
        agent: str = None,
        started: datetime = None,
        ended: datetime = None,
        offset: int = 0,
        limit: int = 100
):
    where = [
        TokenUse.id == id if id else None,
        TokenUse.chat_id == chat_id if chat_id else None,
        TokenUse.message_type == message_type if message_type else None,
        TokenUse.agent == agent if agent else None,
        TokenUse.created >= started if started else None,
        TokenUse.created <= ended if ended else None
    ]
    where = [condition for condition in where if condition is not None]

    count_statement = select(func.count()).select_from(TokenUse).where(*where)
    count = session.exec(count_statement).one()

    statement = select(TokenUse).select_from(TokenUse).where(*where).offset(offset).limit(limit)
    token_uses = session.exec(statement).all()

    return TokenUsesPublic(data=token_uses, count=count)


@router.get('/tool-uses', response_model=ToolUsesPublic)
def get_tool_uses(
        session: SessionDep,
        id: uuid.UUID = None,
        chat_id: uuid.UUID = None,
        toll_name: str = None,
        agent: str = None,
        result: bool = None,
        started: datetime = None,
        ended: datetime = None,
        offset: int = 0,
        limit: int = 100
):
    where = [
        ToolUse.id == id if id else None,
        ToolUse.chat_id == chat_id if chat_id else None,
        ToolUse.tool_name == toll_name if toll_name else None,
        ToolUse.agent == agent if agent else None,
        ToolUse.result == result if result is not None else None,
        ToolUse.created >= started if started else None,
        ToolUse.created <= ended if ended else None
    ]
    where = [condition for condition in where if condition is not None]

    count_statement = select(func.count()).select_from(ToolUse).where(*where)
    count = session.exec(count_statement).one()

    statement = select(ToolUse).select_from(ToolUse).where(*where).offset(offset).limit(limit)
    tool_uses = session.exec(statement).all()

    return ToolUsesPublic(data=tool_uses, count=count)
