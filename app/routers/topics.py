from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import get_api_key
from app.database import get_db

router = APIRouter(prefix="/topics", tags=["Topics"])


@router.get("", response_model=List[schemas.TopicResponse])
def list_topics(
    status: Optional[str] = Query(None, description="Filter by status"),
    category: Optional[str] = Query(None, description="Filter by category"),
    owner: Optional[str] = Query(None, description="Filter by owner"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key),
):
    q = db.query(models.Topic)
    if status:
        q = q.filter(models.Topic.status == status)
    if category:
        q = q.filter(models.Topic.category == category)
    if owner:
        q = q.filter(models.Topic.owner == owner)
    return q.order_by(models.Topic.created_at.desc()).offset(skip).limit(limit).all()


@router.post("", response_model=schemas.TopicResponse, status_code=status.HTTP_201_CREATED)
def create_topic(
    payload: schemas.TopicCreate,
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key),
):
    topic = models.Topic(**payload.model_dump())
    db.add(topic)
    db.commit()
    db.refresh(topic)
    return topic


@router.get("/{topic_id}", response_model=schemas.TopicResponse)
def get_topic(
    topic_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key),
):
    topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


@router.patch("/{topic_id}", response_model=schemas.TopicResponse)
def update_topic(
    topic_id: int,
    payload: schemas.TopicUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key),
):
    topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(topic, field, value)
    topic.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(topic)
    return topic


@router.delete("/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_topic(
    topic_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key),
):
    topic = db.query(models.Topic).filter(models.Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    db.delete(topic)
    db.commit()


# ── Sub-resources ─────────────────────────────────────────────────────────────

@router.get("/{topic_id}/sources", response_model=List[schemas.SourceResponse])
def list_topic_sources(
    topic_id: int,
    type: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key),
):
    if not db.query(models.Topic).filter(models.Topic.id == topic_id).first():
        raise HTTPException(status_code=404, detail="Topic not found")
    q = db.query(models.Source).filter(models.Source.topic_id == topic_id)
    if type:
        q = q.filter(models.Source.type == type)
    return q.order_by(models.Source.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/{topic_id}/insights", response_model=List[schemas.InsightResponse])
def list_topic_insights(
    topic_id: int,
    insight_status: Optional[str] = Query(None, alias="status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key),
):
    if not db.query(models.Topic).filter(models.Topic.id == topic_id).first():
        raise HTTPException(status_code=404, detail="Topic not found")
    q = db.query(models.Insight).filter(models.Insight.topic_id == topic_id)
    if insight_status:
        q = q.filter(models.Insight.status == insight_status)
    return q.order_by(models.Insight.created_at.desc()).offset(skip).limit(limit).all()
