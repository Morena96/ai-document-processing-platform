from app.services.extractors.base import DocumentExtractor
from app.services.extractors.demo import DemoExtractor


def get_extractor() -> DocumentExtractor:
    # Swap this adapter for Gemini/OpenAI/Anthropic without changing API or workflow code.
    return DemoExtractor()
