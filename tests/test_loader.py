"""Tests for ScrapiqLoader — run against a live local Scrapiq instance."""

import httpx
import pytest

from scrapiq_langchain import ScrapiqLoader

ENDPOINT = "http://localhost:8001/v1/extract"


def test_load_markdown_from_real_api():
    loader = ScrapiqLoader(
        url="https://example.com",
        format="markdown",
        endpoint=ENDPOINT,
        timeout=15,
    )
    docs = loader.load()
    assert len(docs) == 1
    doc = docs[0]
    assert "This domain is for use in documentation examples" in doc.page_content
    assert doc.metadata["url"] == "https://example.com"
    assert doc.metadata["source"] == "scrapiq"
    assert doc.metadata["title"] == "Example Domain"


def test_load_text_from_real_api():
    loader = ScrapiqLoader(
        url="https://example.com",
        format="text",
        endpoint=ENDPOINT,
        timeout=15,
    )
    docs = loader.load()
    assert "This domain is for use in documentation examples" in docs[0].page_content


def test_from_urls_multiple():
    loader = ScrapiqLoader.from_urls(
        ["https://example.com", "https://example.org"],
        format="markdown",
        endpoint=ENDPOINT,
        timeout=15,
    )
    docs = loader.load()
    assert len(docs) == 2


def test_bad_url_raises():
    loader = ScrapiqLoader(
        url="https://nonexistent.invalid",
        format="markdown",
        endpoint=ENDPOINT,
        timeout=10,
    )
    with pytest.raises(httpx.HTTPStatusError):
        loader.load()
