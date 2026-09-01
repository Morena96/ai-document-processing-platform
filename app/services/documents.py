import uuid

from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document, DocumentStatus
from app.services.storage import storage


async def create_document(db: AsyncSession, upload: UploadFile) -> Document:
    document_id = str(uuid.uuid4())
    key = f"{document_id}/{upload.filename or 'document'}"
    content = await upload.read()
    await storage.save(key, content)

    document = Document(
        id=document_id,
        filename=upload.filename or "document",
        content_type=upload.content_type or "application/octet-stream",
        storage_key=key,
        status=DocumentStatus.queued,
    )
    db.add(document)
    await db.commit()
    await db.refresh(document)
    return document


async def get_document(db: AsyncSession, document_id: str) -> Document | None:
    result = await db.execute(select(Document).where(Document.id == document_id))
    return result.scalar_one_or_none()
