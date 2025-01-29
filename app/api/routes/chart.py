from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, FileResponse

from app.core.config import settings


router = APIRouter(prefix='/chart', tags=['chart'])


@router.get('/{name}', response_class=HTMLResponse)
async def chart(name: str):
    if Path(settings.CHARTS_FOLDER / name).exists() is False:
        raise HTTPException(status_code=404, detail='Chart not found')
    return FileResponse(settings.CHARTS_FOLDER / name)
