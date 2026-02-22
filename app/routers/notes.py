from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import get_api_key
from app.database import get_db

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get("", response_model=List[schemas.NoteResponse])
def list_notes(
    topic_id: Optional[int] = Query(None),
    source_id: Optional[int] = Query(None),
    author: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key),
):
    q = db.query(models.Note)
    if topic_id is not None:
        q = q.filter(models.Note.topic_id == topic_id)
    if source_id is not None:
        q = q.filter(models.Note.source_id == source_id)
    if author:
        q = q.filter(models.Note.author == author)
    return q.order_by(models.Note.created_at.desc()).offset(skip).limit(limit).all()


@router.post("", response_model=schemas.NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(
    payload: schemas.NoteCreate,
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key),
):
    note = models.Note(**payload.model_dump())
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.get("/{note_id}", response_model=schemas.NoteResponse)
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key),
):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.patch("/{note_id}", response_model=schemas.NoteResponse)
def update_note(
    note_id: int,
    payload: schemas.NoteUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key),
):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(note, field, value)
    note.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(note)
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key),
):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
