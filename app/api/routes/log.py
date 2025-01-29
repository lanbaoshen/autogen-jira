from jinja2 import Template
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.core.config import settings
from app.utils.template import load_template

router = APIRouter(prefix='/log', tags=['log'])

log_html = load_template('log.html')

@router.get('/')
async def get():
    with open(settings.LOG_DIR / 'log.log', 'r') as f:
        html = Template(log_html).render(logs=f.readlines())
        return HTMLResponse(html)
