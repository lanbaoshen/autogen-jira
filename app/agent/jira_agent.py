from collections.abc import Callable

from autogen_agentchat.agents import AssistantAgent
from app.utils.model_client import get_model_client


class JiraAgent(AssistantAgent):
    def __init__(self, *, model_client=None, tools: list[Callable]):
        super().__init__(
            name='jira_agent',
            model_client=model_client if model_client else get_model_client(),
            tools=tools,
            reflect_on_tool_use=True,
            system_message="""
You are a helpful AI assistant. Solve tasks using your tools.
If you need information from the user, ask for it.

Before performing create, update or delete operations, please make sure to get user confirmation          
"""
        )
