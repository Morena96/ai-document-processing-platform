import asyncio

from celery import Celery
from sqlalchemy import select

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.document import Document, DocumentStatus
from app.services.extractors.factory import get_extractor
from app.services.storage import storage

celery_app = Celery("documents", broker=settings.redis_url, backend=settings.redis_url)


async def _process(document_id: str) -> None:
    async with SessionLocal() as db:
        result = await db.execute(select(Document).where(Document.id == document_id))
        document = result.scalar_one()
        document.status = DocumentStatus.processing
        document.error = None
        await db.commit()

        try:
            content = await storage.read(document.storage_key)
            extracted = await get_extractor().extract(
                filename=document.filename,
                content_type=document.content_type,
                content=content,
            )
            document.result = extracted.model_dump(mode="json")
            document.status = DocumentStatus.completed
        except Exception as exc:  # worker boundary: persist failures for retry/inspection
            document.status = DocumentStatus.failed
            document.error = str(exc)[:1000]
        await db.commit()


@celery_app.task(name="documents.process")
def process_document(document_id: str) -> None:
    asyncio.run(_process(document_id))
