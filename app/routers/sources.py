from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import get_api_key
from app.database import get_db

router = APIRouter(prefix="/sources", tags=["Sources"])


@router.get("", response_model=List[schemas.SourceResponse])
def list_sources(
    topic_id: Optional[int] = Query(None, description="Filter by topic"),
    type: Optional[str] = Query(None, description="Filter by source type"),
    credibility: Optional[str] = Query(None, description="Filter by credibility"),
    added_by: Optional[str] = Query(None, description="Filter by contributor"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key),
):
    q = db.query(models.Source)
    if topic_id is not None:
        q = q.filter(models.Source.topic_id == topic_id)
    if type:
        q = q.filter(models.Source.type == type)
    if credibility:
        q = q.filter(models.Source.credibility == credibility)
    if added_by:
        q = q.filter(models.Source.added_by == added_by)
    return q.order_by(models.Source.created_at.desc()).offset(skip).limit(limit).all()


@router.post("", response_model=schemas.SourceResponse, status_code=status.HTTP_201_CREATED)
def create_source(
    payload: schemas.SourceCreate,
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key),
):
    source = models.Source(**payload.model_dump())
    db.add(source)
    db.commit()
    db.refresh(source)
    return source


@router.get("/{source_id}", response_model=schemas.SourceResponse)
def get_source(
    source_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key),
):
    source = db.query(models.Source).filter(models.Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return source


@router.patch("/{source_id}", response_model=schemas.SourceResponse)
def update_source(
    source_id: int,
    payload: schemas.SourceUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key),
):
    source = db.query(models.Source).filter(models.Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(source, field, value)
    source.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(source)
    return source


@router.delete("/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_source(
    source_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key),
):
    source = db.query(models.Source).filter(models.Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    db.delete(source)
    db.commit()
