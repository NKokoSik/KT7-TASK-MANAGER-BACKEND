from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.config import settings
from app.core.limiter import limiter
from app.routers import auth, projects, tasks, notifications, admin
from fastapi.responses import HTMLResponse
from pathlib import Path

app = FastAPI(title=settings.app_name, version="1.0.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(notifications.router)
app.include_router(admin.router)

@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def frontend():
    return (Path(__file__).parent / "static" / "index.html").read_text(encoding="utf-8")
