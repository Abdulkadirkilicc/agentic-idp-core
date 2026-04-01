from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager

from src.domain.models import FailureLog, CorrectionProposal, ApiDocSnippet, GenTestResponse
from src.agents.auto_fixer_agent import AutoFixerAgent
from src.agents.test_generator_agent import TestGeneratorAgent
from src.rag.document_loader import bootstrap_knowledge_base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load demo context into the RAG Vector DB on startup
    print("Initializing Agentic IDP Core...")
    bootstrap_knowledge_base()
    yield
    print("Shutting down Agentic IDP Core...")

from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Agentic IDP (Internal Developer Platform)",
    description="An autonomous API testing and self-healing orchestration layer.",
    version="1.0.0",
    lifespan=lifespan
)

auto_fixer = AutoFixerAgent()
test_generator = TestGeneratorAgent()

# Mount frontend
app.mount("/dashboard", StaticFiles(directory="src/interfaces/web", html=True), name="web")

@app.get("/")
def read_root():
    return RedirectResponse(url="/dashboard/index.html")

@app.get("/health")
def read_health():
    """Health check endpoint for Kubernetes probes."""
    return {"status": "healthy"}

@app.post("/api/v1/analyze-failure", response_model=CorrectionProposal)
def analyze_failure(failure_log: FailureLog):
    """
    Takes a test failure log, uses RAG and an LLM to generate a self-healing patch.
    """
    try:
        proposal = auto_fixer.analyze_and_fix(failure_log)
        return proposal
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/generate-tests", response_model=GenTestResponse)
def generate_tests(api_doc: ApiDocSnippet):
    """
    Takes an OpenAPI endpoint spec, uses RAG and an LLM to generate Pytest scenarios.
    """
    try:
        gen_response = test_generator.generate_tests(api_doc)
        return gen_response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
