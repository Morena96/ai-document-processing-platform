from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.models.document import DocumentStatus


class DocumentResponse(BaseModel):
    id: str
    filename: str
    content_type: str
    status: DocumentStatus
    error: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ExtractionResult(BaseModel):
    document_type: str
    summary: str
    fields: dict[str, Any]
    confidence: float = Field(ge=0, le=1)
