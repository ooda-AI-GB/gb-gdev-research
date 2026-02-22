from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.database import engine, SessionLocal
from app import models
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
