from pathlib import Path
from typing import Literal

import click
from loguru import logger
from pydantic import model_validator, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_ignore_empty=True, extra='ignore'
    )

    PROJECT_NAME: str = 'AutoGen Jira'

    DOMAIN: str = '127.0.0.1:8000'

    @computed_field
    @property
    def server_host(self) -> str:
        return f'http://{self.DOMAIN}'

    SQLITE_DB: str

    MODEL_CLIENT: Literal['azure', 'openai', 'other']

    # OpenAI
    OPENAI_MODEL: str | None = None
    OPENAI_API_KEY: str | None = None
    # Other
    OPENAI_BASE_URL: str | None = None

    # Azure
    AZURE_DEPLOYMENT: str | None = None
    AZURE_MODEL: str | None = None
    AZURE_API_VERSION: str | None = None
    AZURE_ENDPOINT: str | None = None
    AZURE_API_KEY: str | None = None

    @model_validator(mode='after')
    def model_client(self):
        match self.MODEL_CLIENT:
            case 'openai':
                if not all((self.OPENAI_MODEL, self.OPENAI_API_KEY)):
                    raise ValueError(
                        'MODEL_CLIENT is set to openai, '
                        'OPENAI_MODEL and OPENAI_API_KEY must be provided'
                    )
            case 'other':
                if not all((self.OPENAI_MODEL, self.OPENAI_API_KEY, self.OPENAI_BASE_URL)):
                    raise ValueError(
                        'MODEL_CLIENT is set to other, '
                        'OPENAI_MODEL, OPENAI_API_KEY, OPENAI_BASE_URL must be provided'
                    )
            case 'azure':
                if not all((
                    self.AZURE_DEPLOYMENT, self.AZURE_MODEL,
                    self.AZURE_API_VERSION, self.AZURE_ENDPOINT, self.AZURE_API_KEY,
                )):
                    raise ValueError(
                        'MODEL_CLIENT is set to azure, '
                        'AZURE_DEPLOYMENT, AZURE_MODEL, AZURE_API_VERSION, '
                        'AZURE_ENDPOINT and AZURE_API_KEY keys must be provided'
                    )
            case _:
                raise ValueError('MODEL_CLIENT must be either azure, openai or other')

        return self

    STORAGE_DIR: str | Path = Path('storage')
    CHARTS_FOLDER: str | Path = STORAGE_DIR / Path('charts')
    LOG_DIR: str | Path = STORAGE_DIR / Path('logs')

    @model_validator(mode='after')
    def storage_dir(self):
        self.STORAGE_DIR = Path(self.STORAGE_DIR)
        self.CHARTS_FOLDER = Path(self.CHARTS_FOLDER)
        self.LOG_DIR = Path(self.LOG_DIR)

        self.STORAGE_DIR.mkdir(parents=True, exist_ok=True)
        self.CHARTS_FOLDER.mkdir(parents=True, exist_ok=True)
        self.LOG_DIR.mkdir(parents=True, exist_ok=True)

        return self

    SOCKET_TIMEOUT: int = 3600

    def __str__(self):
        ssp = click.style('-' * 26, fg='magenta')
        lsp = click.style('-' * 60, fg='magenta')
        cn = click.style(self.__class__.__name__, fg='magenta')
        info = '\n'.join(
            f'{click.style(f'{k}:', fg='magenta')} {click.style(v, fg='green')}' for k, v in vars(self).items()
        )
        return (
            f'\n{ssp}{cn}{ssp}\n'
            f'{info}\n'
            f'{lsp}'
        )


settings = Settings()

logger.add(settings.LOG_DIR / 'log.log', rotation='1 MB')
logger.info(settings)
