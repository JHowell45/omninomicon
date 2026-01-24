from typing import Sequence

from fastapi import APIRouter
from pydantic import BaseModel
from sqlmodel import select

from omninomicon.deps.db import SessionDep
from omninomicon.deps.embedding_inference import create_embedding
from omninomicon.models.notes import Note, NoteCreate, NotePublic

router = APIRouter(prefix="/notes")


@router.get("/", response_model=list[NotePublic])
def read_notes(session: SessionDep) -> Sequence[Note]:
    return session.exec(select(Note).offset(offset=0).limit(limit=100)).all()


class SearchParams(BaseModel):
    query: str
    limit: int = 100


@router.post("/search", response_model=list[NotePublic])
def search_notes(session: SessionDep, params: SearchParams) -> Sequence[Note]:
    query_embedding: list[float] = create_embedding(params.query).tolist()
    return session.exec(
        select(Note)
        .order_by(Note.embedding.l2_distance(query_embedding))
        .limit(params.limit)
    ).all()


@router.post("/", response_model=NotePublic)
def create_note(session: SessionDep, note_data: NoteCreate) -> Note:
    note = Note.model_validate(note_data)
    session.add(note)
    session.commit()
    session.refresh(note)
    return note
