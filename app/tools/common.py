from typing import Any

from atlassian import Jira

from app.tools._base import ToolBase


class CommonTool(ToolBase):
    """
    The class is a wrapper for the Atlassian class Jira
    Wrap the method in a format that can be called by autogen
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._jira = Jira(*args, **kwargs)

    def jql(
            self,
            jql: str,
            fields: list[str] = None,
            start: int = 0,
            limit: int = 10,
    ) -> list[dict[str, Any]]:
        """
        Get issues from jql search result with specific fields

        Args:
            jql: Jira Query Language query string
            fields: List of fields to return, for example: ['*all', 'key', 'summary']
            start: The index of the first issue to return
            limit: The maximum number of issues to return, this may be restricted by fixed system limits

        Returns:
            Issue dict
        """
        data = self._jira.jql(
            jql=jql,
            fields=','.join(fields) if fields else 'key',
            start=start,
            limit=limit,
        )
        return data
