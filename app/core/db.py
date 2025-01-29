from sqlmodel import create_engine, SQLModel

from app.core.config import settings


engine = create_engine(settings.SQLITE_DB)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)
