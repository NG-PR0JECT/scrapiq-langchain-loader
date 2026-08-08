# Scrapiq LangChain Loader

> LangChain document loader for [Scrapiq](https://github.com/NG-PR0JECT/scrapiq) — turn any URL into clean documents for RAG pipelines.

[Scrapiq](https://github.com/NG-PR0JECT/scrapiq) is a lightweight open-source HTTP API that fetches a web page and returns clean text, markdown, or structured JSON — boilerplate stripped. This loader plugs it into LangChain's document pipeline in ~5 lines.

## Install

```bash
pip install scrapiq-langchain-loader
```

Requires a running Scrapiq instance (see [Scrapiq README](https://github.com/NG-PR0JECT/scrapiq#quick-start) — one Docker command).

## Usage

```python
from scrapiq_langchain import ScrapiqLoader

loader = ScrapiqLoader(
    url="https://en.wikipedia.org/wiki/Retrieval-augmented_generation",
    format="markdown",        # "text" | "markdown" | "json"
    endpoint="http://localhost:8001/v1/extract",
)

docs = loader.load()
for doc in docs:
    print(doc.metadata["url"], len(doc.page_content))
```

Load multiple URLs:

```python
loader = ScrapiqLoader.from_urls(
    [
        "https://example.com/page1",
        "https://example.com/page2",
    ],
    format="text",
)
```

## API

| Param | Default | Description |
|-------|---------|-------------|
| `url` | — | Page to fetch |
| `format` | `markdown` | Output format: `text`, `markdown`, or `json` |
| `endpoint` | `http://localhost:8001/v1/extract` | Scrapiq API endpoint |
| `timeout` | 30 | Request timeout (seconds) |

## Why

RAG quality is bounded by the input text. Scrapiq removes nav, ads, and boilerplate before your chunker ever sees the page — so you embed content, not chrome. Self-hostable, MIT-licensed, no data leaves your network.

## License

MIT
