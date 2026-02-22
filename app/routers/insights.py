from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import get_api_key
from app.database import get_db

router = APIRouter(prefix="/insights", tags=["Insights"])


@router.get("", response_model=List[schemas.InsightResponse])
def list_insights(
    topic_id: Optional[int] = Query(None),
    insight_status: Optional[str] = Query(None, alias="status", description="hypothesis/validated/actionable/archived"),
    confidence: Optional[str] = Query(None),
    impact: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key),
):
    q = db.query(models.Insight)
    if topic_id is not None:
        q = q.filter(models.Insight.topic_id == topic_id)
    if insight_status:
        q = q.filter(models.Insight.status == insight_status)
    if confidence:
        q = q.filter(models.Insight.confidence == confidence)
    if impact:
        q = q.filter(models.Insight.impact == impact)
    if author:
        q = q.filter(models.Insight.author == author)
    return q.order_by(models.Insight.created_at.desc()).offset(skip).limit(limit).all()


@router.post("", response_model=schemas.InsightResponse, status_code=status.HTTP_201_CREATED)
def create_insight(
    payload: schemas.InsightCreate,
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key),
):
    if not db.query(models.Topic).filter(models.Topic.id == payload.topic_id).first():
        raise HTTPException(status_code=404, detail="Topic not found")
    insight = models.Insight(**payload.model_dump())
    db.add(insight)
    db.commit()
    db.refresh(insight)
    return insight


@router.get("/{insight_id}", response_model=schemas.InsightResponse)
def get_insight(
    insight_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key),
):
    insight = db.query(models.Insight).filter(models.Insight.id == insight_id).first()
    if not insight:
        raise HTTPException(status_code=404, detail="Insight not found")
    return insight


@router.patch("/{insight_id}", response_model=schemas.InsightResponse)
def update_insight(
    insight_id: int,
    payload: schemas.InsightUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key),
):
    insight = db.query(models.Insight).filter(models.Insight.id == insight_id).first()
    if not insight:
        raise HTTPException(status_code=404, detail="Insight not found")
    updates = payload.model_dump(exclude_unset=True)
    if "topic_id" in updates:
        if not db.query(models.Topic).filter(models.Topic.id == updates["topic_id"]).first():
            raise HTTPException(status_code=404, detail="Topic not found")
    for field, value in updates.items():
        setattr(insight, field, value)
    insight.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(insight)
    return insight


@router.delete("/{insight_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_insight(
    insight_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key),
):
    insight = db.query(models.Insight).filter(models.Insight.id == insight_id).first()
    if not insight:
        raise HTTPException(status_code=404, detail="Insight not found")
    db.delete(insight)
    db.commit()
