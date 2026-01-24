from typing import Any

from pgvector.sqlalchemy import Vector
from pydantic import computed_field
from sqlmodel import Field, SQLModel

from omninomicon.deps.embedding_inference import create_embedding


class NoteBase(SQLModel):
    text: str


class Note(NoteBase, table=True):
    __tablename__ = "notes"

    id: int | None = Field(default=None, primary_key=True)
    embedding: Any = Field(sa_type=Vector(384))


class NotePublic(NoteBase):
    id: int


class NoteCreate(NoteBase):
    text: str

    @computed_field
    @property
    def embedding(self) -> list[float]:
        return create_embedding(self.text).tolist()
