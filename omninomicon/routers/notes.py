from typing import Sequence

from fastapi import APIRouter
from sqlmodel import select

from omninomicon.deps.db import SessionDep
from omninomicon.models.notes import Note, NotePublic

router = APIRouter(prefix="/notes")


@router.get("", response_model=list[NotePublic])
def read_notes(session: SessionDep) -> Sequence[Note]:
    return session.exec(select(Note).offset(offset=0).limit(limit=100)).all()


@router.post("/search", response_model=list[NotePublic])
def search_notes(session: SessionDep) -> Sequence[Note]:
    return []
