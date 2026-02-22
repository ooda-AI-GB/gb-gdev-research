from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, ForeignKey, JSON
from app.database import Base


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(20), default="active")        # active / paused / completed
    owner = Column(String(255))
    category = Column(String(50))                        # market/technical/competitive/academic/industry
    tags = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String(500), nullable=False)
    url = Column(Text)
    type = Column(String(20))                            # article/paper/report/video/podcast/book/other
    author = Column(String(255))
    publication = Column(String(255))
    published_date = Column(Date, nullable=True)
    summary = Column(Text)
    key_findings = Column(JSON, default=list)
    credibility = Column(String(10), default="medium")   # low / medium / high
    added_by = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="SET NULL"), nullable=True, index=True)
    source_id = Column(Integer, ForeignKey("sources.id", ondelete="SET NULL"), nullable=True, index=True)
    content = Column(Text, nullable=False)
    author = Column(String(255))
    tags = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Insight(Base):
    __tablename__ = "insights"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    content = Column(Text)
    evidence = Column(JSON, default=list)
    confidence = Column(String(10), default="medium")   # low / medium / high
    impact = Column(String(10), default="medium")       # low / medium / high
    status = Column(String(20), default="hypothesis")   # hypothesis/validated/actionable/archived
    author = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    topic_ids = Column(JSON, default=list)
    source_ids = Column(JSON, default=list)
    created_by = Column(String(255))
    shared = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
