from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.document import DocumentStatus
from app.schemas.document import DocumentResponse, ExtractionResult
from app.services.documents import create_document, get_document
from app.workers.tasks import process_document

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_document(
    file: Annotated[UploadFile, File()],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    document = await create_document(db, file)
    process_document.delay(document.id)
    return document


@router.get("/{document_id}", response_model=DocumentResponse)
async def document_status(document_id: str, db: Annotated[AsyncSession, Depends(get_db)]):
    document = await get_document(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.get("/{document_id}/result", response_model=ExtractionResult)
async def document_result(document_id: str, db: Annotated[AsyncSession, Depends(get_db)]):
    document = await get_document(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if document.status != DocumentStatus.completed or not document.result:
        raise HTTPException(status_code=409, detail=f"Document status is {document.status.value}")
    return ExtractionResult.model_validate(document.result)


@router.post("/{document_id}/retry", response_model=DocumentResponse, status_code=202)
async def retry_document(document_id: str, db: Annotated[AsyncSession, Depends(get_db)]):
    document = await get_document(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if document.status == DocumentStatus.processing:
        raise HTTPException(status_code=409, detail="Document is already processing")
    document.status = DocumentStatus.queued
    document.error = None
    await db.commit()
    await db.refresh(document)
    process_document.delay(document.id)
    return document
