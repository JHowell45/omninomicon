from fastapi import APIRouter

from .notes import router as notes_router

router = APIRouter(prefix="/")
router.include_router(notes_router)
