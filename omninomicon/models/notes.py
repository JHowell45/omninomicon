from typing import Any

from pgvector.sqlalchemy import VECTOR
from sqlmodel import Field, SQLModel


class NoteBase(SQLModel):
    text: str
    embedding: Any = Field(sa_type=VECTOR(100))


class Note(NoteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class NotePublic(NoteBase):
    id: int
