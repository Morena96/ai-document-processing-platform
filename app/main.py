from fastapi import FastAPI

from app.api.routes import documents, health
from app.core.config import settings

app = FastAPI(title=settings.app_name, version="1.0.0")
app.include_router(health.router)
app.include_router(documents.router, prefix="/api/v1")
