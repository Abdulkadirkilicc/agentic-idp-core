# Agentic IDP: Autonomous Test & Repair Platform 🚀

Welcome to the **Agentic Internal Developer Platform (IDP)** repository.
This project is engineered to showcase state-of-the-art **AI Platform Engineering** paradigms, merging agent-driven autonomous workflows with Cloud-Native infrastructure and robust backend design.

## 🎯 Architectural Vision

Traditional DevOps toolchains rely on passive pipelines and manual test writing. This platform introduces a paradigm shift: an IDP that **actively reads system state, automatically generates tests based on OpenAPI specs, and proposes self-healing code patches upon CI failure.**

The system is built with a strict **Domain-Driven Design (DDD)** approach, isolating business logic (models) from infrastructure concerns (RAG vectors, LLM integrations) and the presentation layer (FastAPI).

### Key Features & Technical Pillars

1. **Autonomous Agents (LangChain & Python):**
   - **Auto-Fixer Agent:** Analyzes `pytest` stack frames and logs out of CI/CD, leverages an internal Knowledge Base, and outputs actionable, context-aware code patches.
   - **Test-Generator Agent:** Reads Swagger/OpenAPI documentation (in JSON/YAML representations) and autonomously writes Python `pytest` functions covering both "Happy Paths" and edge cases.

2. **RAG (Retrieval-Augmented Generation) & MCP Influence:**
   - Powered by ChromaDB (locally) and `OpenAIEmbeddings`.
   - Adopts principles from the Model Context Protocol (MCP) to inject relevant engineering standards, architectural decisions (CAP constraints, Idempotency rules, gRPC backoff strategies) into the LLM context *before* execution.

3. **Domain-Driven Design (DDD):**
   - Models decoupled using Python `Pydantic`.
   - Layers structured strictly: `src/domain/`, `src/agents/`, `src/infrastructure/`, and `src/interfaces/`.

4. **Cloud-Native & Distributed Systems Focus:**
   - Designed to run inside a Kubernetes cluster as a central internal API.
   - Included `Dockerfile` and `k8s/` deployment manifests.
   - Evaluates the "Consistency vs Availability" trade-offs inside Microservices by ensuring agent suggestions adhere to system rules.

## 📁 Repository Structure

```text
├── Dockerfile                  # Multi-stage Docker config
├── README.md                   # You are here
├── k8s/                        # Kubernetes manifests for deploying the agentic service
├── pyproject.toml / requirements.txt # Python dependencies
└── src/
    ├── agents/                 # Langchain Agents (The 'Brain')
    ├── domain/                 # Pydantic Schemas for APIs, Failure Logs, and Patches
    ├── infrastructure/         # External integrations (Not utilized in the mock, but reserved for GitHub/Jira)
    ├── interfaces/             # Entrypoints: FastAPI Routers
    └── rag/                    # ChromaDB Vector Store & Document ingestion logic
```

## 🚀 Getting Started

### 1. Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file at the root:
```env
# Optional: Overrides the dummy key for actual Langchain execution
OPENAI_API_KEY="sk-proj-..."
```

### 3. Running the Platform Locally

The REST API is exposed via FastAPI and Uvicorn.
```bash
uvicorn src.interfaces.api.main:app --reload --host 0.0.0.0 --port 8000
```
Visit `http://localhost:8000/docs` to see the Agentic IDP endpoints.

---

## 🛠 Usage Examples

### Triggering Self-Healing from CI

Submit a failure log to the `/api/v1/analyze-failure` endpoint.
```json
{
  "test_name": "test_user_registration",
  "error_message": "404 Not Found response when calling POST /users",
  "traceback": "File 'tests/test_users.py', line 45, in test_user_registration ... httpx.HTTPStatusError: 404",
  "file_path": "tests/test_users.py"
}
```

**Agent Response:**
```json
{
  "failure_reason": "The POST route for /users is missing in the FastAPI router.",
  "proposed_fix_description": "Implement the /users route in user_router.py.",
  "patches": [
     {
        "file_path": "src/interfaces/api/user_router.py",
        "action": "create",
         ...
     }
  ],
  "confidence_score": 0.95
}
```

## 👨‍💻 About The Author

This repository showcases my ability to:
- Establish organizational coding standards in Python.
- Bridge the gap between *Generative AI* and *DevOps*.
- Architect Enterprise APIs and define forward-looking tech stack toolchains.

<!-- update 2026-04-13T11:00:00 -->
<!-- update 2026-04-21T12:00:00 -->
<!-- update 2026-04-09T11:00:00 -->
<!-- update 2026-04-07T12:00:00 -->
<!-- update 2026-04-08T15:00:00 -->
<!-- update 2026-04-11T13:00:00 -->
<!-- update 2026-04-21T17:00:00 -->
<!-- update 2026-04-05T14:00:00 -->
## API Documentation Reference
Full API reference available at  endpoint.
