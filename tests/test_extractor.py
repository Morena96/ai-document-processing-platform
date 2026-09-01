import pytest

from app.services.extractors.demo import DemoExtractor


@pytest.mark.asyncio
async def test_demo_extractor_returns_valid_structured_result():
    result = await DemoExtractor().extract(
        filename="invoice-1042.pdf",
        content_type="application/pdf",
        content=b"demo",
    )
    assert result.document_type == "invoice"
    assert result.fields["size_bytes"] == 4
    assert 0 <= result.confidence <= 1
