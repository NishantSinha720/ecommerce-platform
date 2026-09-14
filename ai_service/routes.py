from pydantic import BaseModel
from fastapi import APIRouter
from .rag import build_index, search
from .graph import ask

router = APIRouter(prefix="/api/v1/ai", tags=["AI"])

class QuestionRequest(BaseModel):
    question: str

@router.get("/status")
def status():
    ollama_ok = False
    try:
        import ollama
        ollama.list()
        ollama_ok = True
    except Exception:
        pass
    return {
        "service": "AI RAG",
        "faiss": False,
        "retrieval": True,
        "langgraph": True,
        "ollama": ollama_ok,
        "status": "operational" if ollama_ok else "degraded-but-available",
    }

@router.post("/index")
def index():
    return build_index()

@router.get("/search")
def semantic_search(q: str, top_k: int = 5):
    return {"query": q, "results": search(q, top_k)}

@router.post("/ask")
def ask_ai(request: QuestionRequest):
    return ask(request.question)
