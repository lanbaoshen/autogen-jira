from typing import Literal

from autogen_core.models import ModelInfo
from autogen_ext.models.openai import OpenAIChatCompletionClient, AzureOpenAIChatCompletionClient

from app.core.config import settings


def get_model_client(
        model_client: Literal['azure', 'openai', 'other'] = None,
):
    match model_client if model_client else settings.MODEL_CLIENT:
        case 'openai':
            return OpenAIChatCompletionClient(
                model=settings.OPENAI_MODEL,
                api_key=settings.OPENAI_API_KEY,
            )
        case 'other':
            return OpenAIChatCompletionClient(
                model=settings.OPENAI_MODEL,
                api_key=settings.OPENAI_API_KEY,
                base_url=settings.OPENAI_BASE_URL,
                model_info=ModelInfo(
                    vision=False,
                    function_calling=True,
                    json_output=True,
                    family='unknown'
                )
            )
        case 'azure':
            return AzureOpenAIChatCompletionClient(
                model=settings.AZURE_MODEL,
                api_version=settings.AZURE_API_VERSION,
                azure_deployment=settings.AZURE_DEPLOYMENT,
                azure_endpoint=settings.AZURE_ENDPOINT,
                api_key=settings.AZURE_API_KEY,
            )
