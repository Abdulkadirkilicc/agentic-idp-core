import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from src.domain.models import ApiDocSnippet, GenTestResponse
from src.rag.vector_store import vector_store_manager

class TestGeneratorAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.3,
            openai_api_key=os.environ.get("OPENAI_API_KEY", "dummy-key")
        )
        self.retriever = vector_store_manager.get_retriever()
        
        self.parser = JsonOutputParser(pydantic_object=GenTestResponse)
        
        self.prompt = PromptTemplate(
            template="""You are an autonomous Test Generator Agent working on our Internal Developer Platform (IDP).
Given the API specification below, generate comprehensive pytest test cases.
Also consider our engineering context, if any, retrieved from the RAG store.

Engineering Context:
{context}

API Specification:
Endpoint: {endpoint_path}
Method: {http_method}
Description: {description}
Expected Request: {request_schema}
Expected Response: {response_schema}

Format Instructions:
{format_instructions}

Ensure tests cover happy path and edge cases based on IDP styling (e.g. idempotency, timeouts).
""",
            input_variables=["context", "endpoint_path", "http_method", "description", "request_schema", "response_schema"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        
        self.chain = self.prompt | self.llm | self.parser

    def generate_tests(self, api_doc: ApiDocSnippet) -> GenTestResponse:
        """
        Generates pytest scenarios for a given API specification.
        """
        query = f"API Design Guidelines for {api_doc.http_method} {api_doc.endpoint_path}"
        docs = self.retriever.invoke(query)
        context_text = "\n\n".join([doc.page_content for doc in docs])
        
        if not context_text:
            context_text = "Standard API structure."

        if os.environ.get("OPENAI_API_KEY") in [None, "dummy-key"]:
            # Provide mock response
            return GenTestResponse(
                test_code=f"def test_{api_doc.endpoint_path.strip('/').replace('/', '_')}_success():\n    assert True",
                test_scenarios_covered=["Happy Path Fake Run"]
            )

        response = self.chain.invoke({
            "context": context_text,
            "endpoint_path": api_doc.endpoint_path,
            "http_method": api_doc.http_method,
            "description": api_doc.description,
            "request_schema": api_doc.request_schema,
            "response_schema": api_doc.response_schema
        })
        
        return GenTestResponse(**response)
