import time
from uuid import uuid4

from app.core.config import settings
from app.tools._base import ToolBase


class EChartsTool(ToolBase):
    def save_echarts_html(self, html: str) -> str:
        """
        Save ECharts chart to file and return the url

        Args:
            html: ECharts html content

        Returns:
            URL of the saved chart
        """
        path = settings.CHARTS_FOLDER / f'{time.strftime('%Y-%m-%d', time.localtime())}-{uuid4()}.html'
        with open(path, 'w') as f:
            f.write(html)
        return f'{settings.server_host}/chart/{path.name}'
