import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django
django.setup()

from fastapi import FastAPI
from ai_service.routes import router as ai_router

app = FastAPI(
    title="E-Commerce Platform API",
    version="1.0.0",
)

app.include_router(ai_router)

@app.get("/api/v1/status/")
def status():
    return {
        "service": "FastAPI",
        "django": True,
        "status": "operational",
    }

@app.get("/api/v1/health")
def health():
    return {"status": "ok"}
