import inspect
from typing import Callable


class ToolBase:
    def __init__(self, *args, **kwargs):
        ...

    def tools(self) -> list[Callable]:
        """
        Get all the tools of the class which can be called by autogen.
        This func should not be called by autogen.

        Returns:
            List of tools
        """
        self_ = inspect.currentframe().f_code.co_name
        methods = inspect.getmembers(self, predicate=inspect.ismethod)
        return [
            method for name, method in methods
            if not (name.startswith('_') or name == self_)
        ]
