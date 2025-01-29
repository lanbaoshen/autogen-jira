from pathlib import Path

from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from app.api.main import api_router
from app.core.config import settings
from app.core.db import init_db


init_db()

def custom_generate_unique_id(route: APIRoute) -> str:
    return f'{route.tags[0]}-{route.name}'


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f'/openapi.json',
    generate_unique_id_function=custom_generate_unique_id
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.mount('/static', StaticFiles(directory=Path(__file__).parent / 'static'), name='static')

app.include_router(api_router)
