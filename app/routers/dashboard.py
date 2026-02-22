from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import get_api_key
from app.database import get_db

router = APIRouter(tags=["Dashboard"])

_RECENT_LIMIT = 5
_UNREVIEWED_LIMIT = 10


@router.get("/dashboard", response_model=schemas.DashboardResponse)
def dashboard(
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key),
):
    # Active topics
    active_topics = (
        db.query(models.Topic)
        .filter(models.Topic.status == "active")
        .order_by(models.Topic.updated_at.desc())
        .all()
    )

    # Total source count
    total_sources = db.query(models.Source).count()

    # Most recent insights (any status)
    recent_insights = (
        db.query(models.Insight)
        .order_by(models.Insight.created_at.desc())
        .limit(_RECENT_LIMIT)
        .all()
    )

    # Unreviewed sources: sources with no summary
    unreviewed = (
        db.query(models.Source)
        .filter(
            (models.Source.summary == None) | (models.Source.summary == "")
        )
        .order_by(models.Source.created_at.desc())
        .limit(_UNREVIEWED_LIMIT)
        .all()
    )
    unreviewed_count = (
        db.query(models.Source)
        .filter(
            (models.Source.summary == None) | (models.Source.summary == "")
        )
        .count()
    )

    return schemas.DashboardResponse(
        active_topics_count=len(active_topics),
        active_topics=active_topics,
        total_sources=total_sources,
        recent_insights=recent_insights,
        unreviewed_sources_count=unreviewed_count,
        unreviewed_sources=unreviewed,
    )
