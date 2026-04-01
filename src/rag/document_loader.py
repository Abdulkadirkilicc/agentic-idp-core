from langchain_core.documents import Document
from .vector_store import vector_store_manager

def bootstrap_knowledge_base():
    """
    Simulates loading previous test resolutions and IDP standard engineering practices
    into the Vector Store for the RAG Agent to use.
    """
    initial_docs = [
        Document(
            page_content="When a test fails with 'status code 404 instead of 200', it often means the endpoint route is missing or misconfigured in the FastAPI router.",
            metadata={"source": "past_issues_db", "topic": "routing_errors"}
        ),
        Document(
            page_content="For gRPC connectivity errors like 'UNAVAILABLE', the fix is usually to implement a retry mechanism with exponential backoff.",
            metadata={"source": "engineering_guidelines", "topic": "grpc_resilience"}
        ),
        Document(
            page_content="In our Internal Developer Platform, all REST requests that mutate state (POST, PUT, DELETE) MUST contain an X-Idempotency-Key header.",
            metadata={"source": "api_standards", "topic": "idempotency"}
        )
    ]
    
    vector_store_manager.add_documents(initial_docs)
    print("Knowledge base bootstrapped with initial documents.")
