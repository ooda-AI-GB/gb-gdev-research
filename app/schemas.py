from __future__ import annotations
from datetime import date, datetime
from typing import List, Optional, Any
from pydantic import BaseModel, ConfigDict


# ── Topic ────────────────────────────────────────────────────────────────────

class TopicCreate(BaseModel):
    name: str
    description: Optional[str] = None
    status: str = "active"           # active / paused / completed
    owner: Optional[str] = None
    category: Optional[str] = None   # market/technical/competitive/academic/industry
    tags: List[str] = []


class TopicUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    owner: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None


class TopicResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    status: str
    owner: Optional[str]
    category: Optional[str]
    tags: List[Any]
    created_at: datetime
    updated_at: datetime


# ── Source ───────────────────────────────────────────────────────────────────

class SourceCreate(BaseModel):
    topic_id: Optional[int] = None
    title: str
    url: Optional[str] = None
    type: Optional[str] = None       # article/paper/report/video/podcast/book/other
    author: Optional[str] = None
    publication: Optional[str] = None
    published_date: Optional[date] = None
    summary: Optional[str] = None
    key_findings: List[str] = []
    credibility: str = "medium"      # low / medium / high
    added_by: Optional[str] = None


class SourceUpdate(BaseModel):
    topic_id: Optional[int] = None
    title: Optional[str] = None
    url: Optional[str] = None
    type: Optional[str] = None
    author: Optional[str] = None
    publication: Optional[str] = None
    published_date: Optional[date] = None
    summary: Optional[str] = None
    key_findings: Optional[List[str]] = None
    credibility: Optional[str] = None
    added_by: Optional[str] = None


class SourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    topic_id: Optional[int]
    title: str
    url: Optional[str]
    type: Optional[str]
    author: Optional[str]
    publication: Optional[str]
    published_date: Optional[date]
    summary: Optional[str]
    key_findings: List[Any]
    credibility: str
    added_by: Optional[str]
    created_at: datetime
    updated_at: datetime


# ── Note ─────────────────────────────────────────────────────────────────────

class NoteCreate(BaseModel):
    topic_id: Optional[int] = None
    source_id: Optional[int] = None
    content: str
    author: Optional[str] = None
    tags: List[str] = []


class NoteUpdate(BaseModel):
    topic_id: Optional[int] = None
    source_id: Optional[int] = None
    content: Optional[str] = None
    author: Optional[str] = None
    tags: Optional[List[str]] = None


class NoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    topic_id: Optional[int]
    source_id: Optional[int]
    content: str
    author: Optional[str]
    tags: List[Any]
    created_at: datetime
    updated_at: datetime


# ── Insight ───────────────────────────────────────────────────────────────────

class InsightCreate(BaseModel):
    topic_id: int
    title: str
    content: Optional[str] = None
    evidence: List[str] = []
    confidence: str = "medium"       # low / medium / high
    impact: str = "medium"           # low / medium / high
    status: str = "hypothesis"       # hypothesis/validated/actionable/archived
    author: Optional[str] = None


class InsightUpdate(BaseModel):
    topic_id: Optional[int] = None
    title: Optional[str] = None
    content: Optional[str] = None
    evidence: Optional[List[str]] = None
    confidence: Optional[str] = None
    impact: Optional[str] = None
    status: Optional[str] = None
    author: Optional[str] = None


class InsightResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    topic_id: int
    title: str
    content: Optional[str]
    evidence: List[Any]
    confidence: str
    impact: str
    status: str
    author: Optional[str]
    created_at: datetime
    updated_at: datetime


# ── Collection ────────────────────────────────────────────────────────────────

class CollectionCreate(BaseModel):
    name: str
    description: Optional[str] = None
    topic_ids: List[int] = []
    source_ids: List[int] = []
    created_by: Optional[str] = None
    shared: bool = False


class CollectionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    topic_ids: Optional[List[int]] = None
    source_ids: Optional[List[int]] = None
    created_by: Optional[str] = None
    shared: Optional[bool] = None


class CollectionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str]
    topic_ids: List[Any]
    source_ids: List[Any]
    created_by: Optional[str]
    shared: bool
    created_at: datetime
    updated_at: datetime


# ── Search ────────────────────────────────────────────────────────────────────

class SearchResult(BaseModel):
    result_type: str           # "source" | "note" | "insight"
    id: int
    title: Optional[str]      # sources and insights have titles
    content: Optional[str]    # notes and insights have content
    topic_id: Optional[int]
    created_at: datetime


class SearchResponse(BaseModel):
    query: str
    total: int
    results: List[SearchResult]


# ── Dashboard ─────────────────────────────────────────────────────────────────

class DashboardResponse(BaseModel):
    active_topics_count: int
    active_topics: List[TopicResponse]
    total_sources: int
    recent_insights: List[InsightResponse]
    unreviewed_sources_count: int
    unreviewed_sources: List[SourceResponse]
