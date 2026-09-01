from abc import ABC, abstractmethod

from app.schemas.document import ExtractionResult


class DocumentExtractor(ABC):
    @abstractmethod
    async def extract(self, *, filename: str, content_type: str, content: bytes) -> ExtractionResult:
        raise NotImplementedError
