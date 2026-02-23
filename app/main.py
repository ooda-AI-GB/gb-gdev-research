from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import func as sqlfunc

from app.database import engine, SessionLocal, get_db
from app import models
from app.models import Topic, Source, Note, Insight, Collection
from app.seed import seed
from app.routers import topics, sources, notes, insights, collections, search, dashboard

API_PREFIX = "/api/v1"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables on startup
    models.Base.metadata.create_all(bind=engine)
    # Seed sample data
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="Research Pro",
    description=(
        "Research knowledge management and discovery API for teams.\n\n"
        "Authenticate every request with the `X-API-Token` header.\n"
        "Set the `GDEV_API_TOKEN` environment variable to configure the expected token (default: `dev-token`)."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

from viv_auth import init_auth
User, require_auth = init_auth(app, engine, models.Base, get_db, app_name="Research Pro")

# ── Root dashboard (no auth) ──────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def root_dashboard(db: Session = Depends(get_db), user=Depends(require_auth)):
    topic_count = db.query(sqlfunc.count(Topic.id)).scalar() or 0
    source_count = db.query(sqlfunc.count(Source.id)).scalar() or 0
    note_count = db.query(sqlfunc.count(Note.id)).scalar() or 0
    insight_count = db.query(sqlfunc.count(Insight.id)).scalar() or 0
    collection_count = db.query(sqlfunc.count(Collection.id)).scalar() or 0
    active_topics = db.query(sqlfunc.count(Topic.id)).filter(Topic.status == "active").scalar() or 0
    recent = db.query(Topic).order_by(Topic.created_at.desc()).limit(8).all()
    status_colors = {"active": "#34c759", "paused": "#f5a623", "completed": "#4f8ef7"}
    rows = ""
    for t in recent:
        sc = status_colors.get(t.status, "#7f8c9b")
        rows += f'<tr><td>{t.name}</td><td>{t.category or "—"}</td><td><span style="color:{sc};font-weight:600">{t.status}</span></td><td>{t.owner or "—"}</td></tr>'
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>Research Pro</title>
<style>
:root{{--primary:#4f8ef7;--success:#34c759;--warning:#f5a623;--danger:#e74c3c;--bg:#1a1f36;--bg-light:#f5f7fa;--card:#fff;--text:#2c3e50;--muted:#7f8c9b;--border:#e1e5eb}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:system-ui,-apple-system,sans-serif;background:var(--bg-light);color:var(--text);display:flex;min-height:100vh}}
.sidebar{{width:240px;background:var(--bg);color:#fff;display:flex;flex-direction:column;flex-shrink:0}}
.logo{{padding:1.5rem;font-size:1.4rem;font-weight:700}}
.nav-links{{flex:1;padding:0 1rem}}
.nav-link{{display:block;padding:.75rem 1rem;color:#cbd5e1;text-decoration:none;border-radius:6px;margin-bottom:.25rem}}
.nav-link:hover,.nav-link.active{{background:rgba(255,255,255,.15);color:#fff}}
.main{{flex:1;padding:2rem;overflow-y:auto}}
h1{{font-size:1.8rem;margin-bottom:1.5rem}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:1rem;margin-bottom:2rem}}
.card{{background:var(--card);border-radius:10px;padding:1.5rem;border:1px solid var(--border)}}
.card .label{{font-size:.85rem;color:var(--muted);margin-bottom:.25rem}}
.card .value{{font-size:1.6rem;font-weight:700}}
.card .value.blue{{color:var(--primary)}} .card .value.green{{color:var(--success)}} .card .value.orange{{color:var(--warning)}}
table{{width:100%;border-collapse:collapse;background:var(--card);border-radius:10px;overflow:hidden;border:1px solid var(--border)}}
th,td{{padding:.75rem 1rem;text-align:left;border-bottom:1px solid var(--border)}}
th{{background:var(--bg);color:#fff;font-weight:600;font-size:.85rem;text-transform:uppercase;letter-spacing:.5px}}
tr:last-child td{{border-bottom:none}}
.section-title{{font-size:1.1rem;font-weight:600;margin-bottom:1rem}}
a.api-link{{display:inline-block;margin-top:1rem;padding:.5rem 1rem;background:var(--primary);color:#fff;border-radius:6px;text-decoration:none;font-size:.9rem}}
</style></head><body>
<div class="sidebar">
  <div class="logo">Research Pro</div>
  <div class="nav-links">
    <a href="/" class="nav-link active">Dashboard</a>
    <a href="/docs" class="nav-link">API Docs</a>
    <a href="/auth/logout" class="nav-link" style="border-top:1px solid rgba(255,255,255,.1);padding-top:.75rem;margin-top:.5rem;color:#f87171">Logout</a>
  </div>
</div>
<div class="main">
  <h1>Dashboard</h1>
  <div class="cards">
    <div class="card"><div class="label">Topics</div><div class="value blue">{topic_count}</div></div>
    <div class="card"><div class="label">Active</div><div class="value green">{active_topics}</div></div>
    <div class="card"><div class="label">Sources</div><div class="value">{source_count}</div></div>
    <div class="card"><div class="label">Notes</div><div class="value">{note_count}</div></div>
    <div class="card"><div class="label">Insights</div><div class="value orange">{insight_count}</div></div>
    <div class="card"><div class="label">Collections</div><div class="value">{collection_count}</div></div>
  </div>
  <div class="section-title">Recent Topics</div>
  <table><thead><tr><th>Name</th><th>Category</th><th>Status</th><th>Owner</th></tr></thead><tbody>{rows if rows else '<tr><td colspan="4" style="text-align:center;color:var(--muted)">No topics yet</td></tr>'}</tbody></table>
  <a href="/docs" class="api-link">API Documentation &rarr;</a>
</div></body></html>"""


# ── Health check (no auth) ────────────────────────────────────────────────────

@app.get("/health", tags=["Health"], include_in_schema=True)
def health():
    return JSONResponse({"status": "ok"})


# ── Versioned routers ─────────────────────────────────────────────────────────

app.include_router(topics.router,      prefix=API_PREFIX)
app.include_router(sources.router,     prefix=API_PREFIX)
app.include_router(notes.router,       prefix=API_PREFIX)
app.include_router(insights.router,    prefix=API_PREFIX)
app.include_router(collections.router, prefix=API_PREFIX)
app.include_router(search.router,      prefix=API_PREFIX)
app.include_router(dashboard.router,   prefix=API_PREFIX)
