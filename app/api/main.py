from fastapi import APIRouter

from app.api.routes import chat, chart, meas, log


api_router = APIRouter()
api_router.include_router(chat.router)
api_router.include_router(chart.router)
api_router.include_router(meas.router)
api_router.include_router(log.router)
