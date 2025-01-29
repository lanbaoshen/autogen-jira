import asyncio
import uuid

from atlassian import Jira
from autogen_agentchat.base import Response
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from fastapi import APIRouter, WebSocket
from fastapi.responses import HTMLResponse
from jinja2 import Template
from loguru import logger
from starlette.websockets import WebSocketDisconnect

from app.agent import JiraAgent
from app.api.deps import SessionDep
from app.core.config import settings
from app.crud.chat import create_chat
from app.crud.token_use import create_token_use
from app.crud.tool_use import create_tool_use
from app.models import ChatCreate, TokenUseCreate, ToolUseCreate
from app.utils.connection_manager import manager
from app.utils.template import load_template
from app.tools import tools

router = APIRouter(prefix='/chat', tags=['chat'])

chat_html = load_template('chat.html')

@router.get('/')
async def get():
    html = Template(chat_html).render(
        tools=tools,
        ws_url=f'ws://{settings.DOMAIN}{router.prefix}',
        inputTemplates=[
            {'name': 'Help', 'detail': 'What can u do for me'},
            {'name': 'Search My Issue', 'detail': 'Search issue which assign to me or report to me, field summary, limit 5'},
        ]
    )
    return HTMLResponse(html)


@router.websocket('/{socket_id}')
async def chat(
        websocket: WebSocket,
        socket_id: str,
        session: SessionDep
):
    await manager.connect(websocket)

    params = await websocket.receive_json()
    url, token = params.get('url'), params.get('token')
    selected_tools = params.get('selected_tools')

    try:
        username = Jira(url=url, token=token).myself().get('name')
    except Exception as msg:
        logger.error(f'[{socket_id} {msg}]')
        await manager.send_personal_message('Jira URL or Token is invalid', websocket)
        return

    # Init agent
    tools_ = [
        tool
        for selected_tool in selected_tools if (info := tools.get(selected_tool))
        for tool in info.get('tool')(url=url, token=token).tools()
    ]

    agent = JiraAgent(tools=tools_)
    chat_ = create_chat(session=session, chat_create=ChatCreate(id=uuid.UUID(socket_id), username=username))

    tool_use_dict = {}
    try:
        while True:
            try:
                await manager.send_personal_message('Need user input', websocket)
                user_input = await asyncio.wait_for(websocket.receive_text(), settings.SOCKET_TIMEOUT)
                logger.info(f'[{chat_.id}][{username}] {user_input}')
            except asyncio.TimeoutError:
                msg = f"It's bee {settings.SOCKET_TIMEOUT} seconds with no response, I'm leaving now."
                logger.warning(f'[{chat_.id}][{agent.name}] {msg}')
                await manager.send_personal_message(msg, websocket)
                break

            if user_input.lower().strip() == '/reset':
                await agent.on_reset(cancellation_token=CancellationToken())
                await manager.send_personal_message('You have faded from my memory.', websocket)
                continue

            async for response in agent.on_messages_stream(
                messages=[TextMessage(content=user_input, source='user')],
                cancellation_token=CancellationToken()
            ):
                if isinstance(response, Response):
                    msg = response.chat_message.content
                    logger.info(f'[{chat_.id}][{agent.name}] {msg}')
                    await manager.send_personal_message(msg, websocket)

                    create_token_use(session=session, token_use_create=TokenUseCreate(
                        chat_id=chat_.id,
                        message_type=response.chat_message.type,
                        agent=agent.name,
                        prompt_tokens=response.chat_message.models_usage.prompt_tokens,
                        completion_tokens=response.chat_message.models_usage.completion_tokens,
                    ))

                    for message in response.inner_messages:
                        if message.type == 'ToolCallRequestEvent':
                            for content in message.content:
                                tool_use_dict[content.id] = content.name

                            create_token_use(session=session, token_use_create=TokenUseCreate(
                                chat_id=chat_.id,
                                message_type=message.type,
                                agent=agent.name,
                                prompt_tokens=message.models_usage.prompt_tokens,
                                completion_tokens=message.models_usage.completion_tokens,
                            ))
                        elif message.type == 'ToolCallExecutionEvent':
                            for content in message.content:
                                tool_name = tool_use_dict.pop(content.call_id)

                                create_tool_use(session=session, tool_use_create=ToolUseCreate(
                                    chat_id=chat_.id,
                                    tool_name=tool_name,
                                    agent=agent.name,
                                    result=not content.content.startswith('Error:'),
                                ))
                else:
                    logger.debug(f'[{chat_.id}][{agent.name}] {response}')
    except WebSocketDisconnect:
        manager.disconnect(websocket)
