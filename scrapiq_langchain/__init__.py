"""Scrapiq LangChain document loader."""

from __future__ import annotations

from typing import Any, Iterator, List, Optional

import httpx

try:
    from langchain_core.documents import Document
    from langchain_core.document_loaders import BaseLoader
except ImportError:  # pragma: no cover
    Document = Any
    BaseLoader = object


class ScrapiqLoader(BaseLoader):
    """Load documents from URLs via the Scrapiq extraction API.

    Scrapiq (https://github.com/NG-PR0JECT/scrapiq) fetches a page and
    returns clean text, markdown, or structured JSON with boilerplate
    stripped — ideal as a first step in a RAG ingestion pipeline.
    """

    def __init__(
        self,
        url: str | List[str],
        format: str = "markdown",
        endpoint: str = "http://localhost:8001/v1/extract",
        timeout: float = 30.0,
        client: Optional[httpx.Client] = None,
    ) -> None:
        self.url = url
        self.format = format
        self.endpoint = endpoint
        self.timeout = timeout
        self._client = client

    @classmethod
    def from_urls(
        cls,
        urls: List[str],
        **kwargs: Any,
    ) -> "ScrapiqLoader":
        """Create a loader that yields one Document per URL."""
        return cls(url=urls, **kwargs)

    def _fetch(self, url: str) -> dict:
        payload = {"url": url, "format": self.format}
        if self._client is not None:
            resp = self._client.post(self.endpoint, json=payload, timeout=self.timeout)
        else:
            with httpx.Client() as client:
                resp = client.post(self.endpoint, json=payload, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def lazy_load(self) -> Iterator[Document]:
        if isinstance(self.url, list):
            for u in self.url:
                yield from self._lazy_load_one(u)
        else:
            yield from self._lazy_load_one(self.url)

    def _lazy_load_one(self, url: str) -> Iterator[Document]:
        data = self._fetch(url)
        content = data.get("content") or data.get("text") or ""
        metadata = {
            "url": url,
            "format": self.format,
            "source": "scrapiq",
        }
        metadata.update(data.get("metadata", {}))
        yield Document(page_content=str(content), metadata=metadata)
