from sqlmodel import Session

from app.models import TokenUse, TokenUseCreate


def create_token_use(*, session: Session, token_use_create: TokenUseCreate) -> TokenUse:
    token_use = TokenUse.model_validate(token_use_create)
    session.add(token_use)
    session.commit()
    session.refresh(token_use)
    return token_use
