from sqlmodel import Session

from app.models import ChatCreate, Chat


def create_chat(*, session: Session, chat_create: ChatCreate) -> Chat:
    chat = Chat.model_validate(chat_create)
    session.add(chat)
    session.commit()
    session.refresh(chat)
    return chat
