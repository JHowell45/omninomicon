from typing import Annotated, Generator

from fastapi import Depends
from sqlmodel import Session, create_engine

from .config import Settings, get_settings

setting: Settings = get_settings()

engine = create_engine(str(settings))


def get_session() -> Generator[Session]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
