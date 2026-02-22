from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import get_api_key
from app.database import get_db

router = APIRouter(tags=["Search"])


@router.get("/search", response_model=schemas.SearchResponse)
def search(
    q: str = Query(..., min_length=1, description="Keyword to search across sources, notes, and insights"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key),
):
    pattern = f"%{q}%"
    results: List[schemas.SearchResult] = []

    # Search sources (title + summary)
    sources = (
        db.query(models.Source)
        .filter(
            models.Source.title.ilike(pattern) | models.Source.summary.ilike(pattern)
        )
        .all()
    )
    for s in sources:
        results.append(
            schemas.SearchResult(
                result_type="source",
                id=s.id,
                title=s.title,
                content=s.summary,
                topic_id=s.topic_id,
                created_at=s.created_at,
            )
        )

    # Search notes (content)
    notes = db.query(models.Note).filter(models.Note.content.ilike(pattern)).all()
    for n in notes:
        results.append(
            schemas.SearchResult(
                result_type="note",
                id=n.id,
                title=None,
                content=n.content,
                topic_id=n.topic_id,
                created_at=n.created_at,
            )
        )

    # Search insights (title + content)
    insights = (
        db.query(models.Insight)
        .filter(
            models.Insight.title.ilike(pattern) | models.Insight.content.ilike(pattern)
        )
        .all()
    )
    for i in insights:
        results.append(
            schemas.SearchResult(
                result_type="insight",
                id=i.id,
                title=i.title,
                content=i.content,
                topic_id=i.topic_id,
                created_at=i.created_at,
            )
        )

    # Sort combined results by recency and paginate
    results.sort(key=lambda r: r.created_at, reverse=True)
    total = len(results)
    paginated = results[skip : skip + limit]

    return schemas.SearchResponse(query=q, total=total, results=paginated)
