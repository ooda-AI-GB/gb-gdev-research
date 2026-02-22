from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.auth import get_api_key
from app.database import get_db

router = APIRouter(prefix="/collections", tags=["Collections"])


@router.get("", response_model=List[schemas.CollectionResponse])
def list_collections(
    created_by: Optional[str] = Query(None),
    shared: Optional[bool] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key),
):
    q = db.query(models.Collection)
    if created_by:
        q = q.filter(models.Collection.created_by == created_by)
    if shared is not None:
        q = q.filter(models.Collection.shared == shared)
    return q.order_by(models.Collection.created_at.desc()).offset(skip).limit(limit).all()


@router.post("", response_model=schemas.CollectionResponse, status_code=status.HTTP_201_CREATED)
def create_collection(
    payload: schemas.CollectionCreate,
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key),
):
    collection = models.Collection(**payload.model_dump())
    db.add(collection)
    db.commit()
    db.refresh(collection)
    return collection


@router.get("/{collection_id}", response_model=schemas.CollectionResponse)
def get_collection(
    collection_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key),
):
    collection = db.query(models.Collection).filter(models.Collection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


@router.patch("/{collection_id}", response_model=schemas.CollectionResponse)
def update_collection(
    collection_id: int,
    payload: schemas.CollectionUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key),
):
    collection = db.query(models.Collection).filter(models.Collection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(collection, field, value)
    collection.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(collection)
    return collection


@router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_collection(
    collection_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key),
):
    collection = db.query(models.Collection).filter(models.Collection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    db.delete(collection)
    db.commit()
