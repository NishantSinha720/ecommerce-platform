# System Architecture

## Frontend

React + Vite provides:

- Login
- Dashboard
- Products
- Inventory
- Orders
- Analytics
- AI

## Reverse Proxy

Nginx serves React and routes API traffic.

## Django

Django REST Framework manages:

- Users
- Products
- Categories
- Inventory
- Orders
- Analytics

## FastAPI

FastAPI provides high-performance services including AI/RAG functionality.

## Database

MySQL stores transactional application data.

## Redis

Redis provides caching and Celery task infrastructure.

## Celery

Celery executes asynchronous/background jobs.

## AI

The AI layer supports:

- Retrieval
- RAG
- Ollama
- LangGraph
- Vector-search-compatible architecture
- Deterministic fallback
