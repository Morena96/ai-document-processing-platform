# AI Document Processing Platform

A production-style asynchronous document-processing service built with FastAPI. Documents are uploaded through the API, persisted, queued for background processing, passed through an extractor abstraction, and returned as structured results.

## Architecture

```text
Client
  |
  v
FastAPI API ------> PostgreSQL
  |                     ^
  |                     |
  `----> Redis/Celery --> Worker
                           |
                           v
                    Extractor Provider
                    (demo / LLM adapter)
```

## What it demonstrates

- FastAPI API design
- asynchronous document workflows
- background workers with Celery
- PostgreSQL persistence
- file-storage abstraction
- provider-based extraction architecture
- structured extraction results
- Docker Compose development environment
- automated tests and CI

The default extractor is deterministic so the repository runs without external API credentials. A production LLM or document-intelligence provider can be implemented behind the same interface.

## Tech stack

`Python` `FastAPI` `SQLAlchemy` `PostgreSQL` `Redis` `Celery` `Docker` `Pytest`

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

API docs: `http://localhost:8000/docs`

## Typical workflow

1. Upload a document.
2. The API creates a processing record.
3. A background job processes the document.
4. The configured extractor returns structured data.
5. Status and results are persisted and available through the API.

## Engineering focus

This repository focuses on the architecture around AI/document processing rather than hiding everything inside a single request handler. Expensive work is asynchronous, extractor implementations are replaceable, and persistence/storage concerns are separated from the HTTP layer.

## Author

**Dovlet Aydogdyyev** — Senior Software Engineer  
Python · Django · FastAPI · Flutter · React
