from typing import Any

from pgvector.sqlalchemy import Vector
from sqlmodel import Field, SQLModel


class NoteBase(SQLModel):
    text: str
    embedding: Any = Field(sa_type=Vector(384))


class Note(NoteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class NotePublic(NoteBase):
    id: int


class NoteCreate(SQLModel):
    text: str
