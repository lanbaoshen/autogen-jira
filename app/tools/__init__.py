from .common import CommonTool
from .echarts import EChartsTool


tools = {
    'common': {'desc': 'Common tools, like jql, set label, add comment', 'tool': CommonTool},
    'echarts': {'desc': 'Create ECharts html chart', 'tool': EChartsTool},
}
