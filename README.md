# E-Commerce Platform — Full Stack

**Developed by Nishant Sinha**

# E-Commerce Platform â€” Full Stack

A clean rebuild of an Order & Inventory Management Platform.

## Stack

- React + Vite
- Django + Django REST Framework
- JWT authentication
- MySQL
- Redis
- Celery
- FastAPI
- Pandas + scikit-learn analytics
- Optional Ollama + FAISS RAG
- Nginx
- Docker Compose

## Quick start

Requirements:
- Docker Desktop
- Git
- Optional: Ollama on the host for local AI

From the project root:

```powershell
Copy-Item .env.example .env
docker compose up -d --build
```

Then open:

- Frontend: http://localhost/
- Login: http://localhost/login
- Django API: http://localhost/api/products/
- FastAPI: http://localhost/api/v1/status/
- AI status: http://localhost/api/v1/ai/status
- FastAPI docs: http://localhost/api/v1/docs

Create a test account from the React registration screen, or use:

```text
username: admin
password: Admin123!
```

The `bootstrap` service creates that account automatically.

## Useful commands

```powershell
docker compose ps
docker compose logs -f django
docker compose logs -f fastapi
docker compose logs -f celery
docker compose down
```

## Local development without Docker

Backend:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Frontend:

```powershell
cd frontend
npm install
npm run dev
```

For local development, set `DB_ENGINE=sqlite` in `.env`.

## AI

AI endpoints never prevent the rest of the platform from starting. If Ollama is unavailable, `/api/v1/ai/status` reports the degraded AI state and the question endpoint returns a useful fallback based on retrieved catalog context.

If Ollama is installed:

```powershell
ollama pull llama3.2
ollama pull nomic-embed-text
```

Then:

```text
POST /api/v1/ai/index
POST /api/v1/ai/ask
GET  /api/v1/ai/search?q=laptop
```

## Architecture

```text
Browser
   |
 Nginx :80
   |-------------------- React static files
   |
   +---- /api/ ------------ Django + DRF
   |
   +---- /api/v1/ --------- FastAPI
                              |
                              +--- Ollama / optional RAG

Django ---- MySQL
Django ---- Redis ---- Celery
```

