from sqlmodel import Session

from app.models import ToolUse, ToolUseCreate


def create_tool_use(*, session: Session, tool_use_create: ToolUseCreate) -> ToolUse:
    tool_use = ToolUse.model_validate(tool_use_create)
    session.add(tool_use)
    session.commit()
    session.refresh(tool_use)
    return tool_use
