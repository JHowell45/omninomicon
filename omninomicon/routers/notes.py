from typing import Sequence

from fastapi import APIRouter
from sqlmodel import select

from omninomicon.deps.db import SessionDep
from omninomicon.deps.embedding_inference import create_embedding
from omninomicon.models.notes import Note, NoteBase, NotePublic

router = APIRouter(prefix="/notes")


@router.get("/", response_model=list[NotePublic])
def read_notes(session: SessionDep) -> Sequence[Note]:
    return session.exec(select(Note).offset(offset=0).limit(limit=100)).all()


@router.post("/search", response_model=list[NotePublic])
def search_notes(session: SessionDep) -> Sequence[Note]:
    return []


@router.post("/", response_model=NotePublic)
def create_note(session: SessionDep, note_text: str) -> Note:
    note_data = NoteBase(text=note_text, embedding=create_embedding(note_text))
    note = Note.model_validate(note_data)
    session.add(note)
    session.commit()
    session.refresh(note)
    return note
