from pathlib import Path

from app.schemas.document import ExtractionResult
from app.services.extractors.base import DocumentExtractor


class DemoExtractor(DocumentExtractor):
    async def extract(self, *, filename: str, content_type: str, content: bytes) -> ExtractionResult:
        suffix = Path(filename).suffix.lower()
        document_type = "invoice" if "invoice" in filename.lower() else (suffix.lstrip(".") or "document")
        return ExtractionResult(
            document_type=document_type,
            summary=f"Demo extraction for {filename}",
            fields={
                "filename": filename,
                "content_type": content_type,
                "size_bytes": len(content),
            },
            confidence=0.95,
        )
