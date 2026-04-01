import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from src.domain.models import FailureLog, CorrectionProposal, CodePatch
from src.rag.vector_store import vector_store_manager

class AutoFixerAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.2,
            openai_api_key=os.environ.get("OPENAI_API_KEY", "dummy-key")
        )
        self.retriever = vector_store_manager.get_retriever()
        
        # We use a JSON Output parser linked to our Pydantic model
        self.parser = JsonOutputParser(pydantic_object=CorrectionProposal)
        
        self.prompt = PromptTemplate(
            template="""You are an expert AI Platform Engineer and autonomous debugging agent.
Given a test failure log and some contextual knowledge from past resolutions or API guidelines, propose a fix.

Context from Knowledge Base:
{context}

Failure Details:
Test Name: {test_name}
Error Message: {error_message}
Traceback: {traceback}

Format Instructions:
{format_instructions}

Please analyze the failure, consider the context, and output your proposed fix.
""",
            input_variables=["context", "test_name", "error_message", "traceback"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        
        self.chain = self.prompt | self.llm | self.parser

    def analyze_and_fix(self, failure_log: FailureLog) -> CorrectionProposal:
        """
        Takes a FailureLog, retrieves relevant context from RAG, and generates a correction proposal.
        """
        # Step 1: Query RAG for context
        query = f"Test failed: {failure_log.test_name}. Error: {failure_log.error_message}"
        docs = self.retriever.invoke(query)
        context_text = "\n\n".join([doc.page_content for doc in docs])
        
        if not context_text:
            context_text = "No specific context found in IDP knowledge base."

        # Step 2: Invoke Chain (Mocked for testing if no genuine API Key is present)
        if os.environ.get("OPENAI_API_KEY") in [None, "dummy-key"]:
            # Return a mocked response for demo purposes
            return CorrectionProposal(
                failure_reason="Mocked reason: Endpoint mapping is incorrect.",
                proposed_fix_description="Add the missing route to the FastAPI router.",
                patches=[
                    CodePatch(
                        file_path="src/interfaces/api/main.py",
                        action="modify",
                        old_code_snippet="# No route implementation",
                        new_code_snippet="@app.get('/dummy')\ndef dummy(): return {'status': 'ok'}"
                    )
                ],
                confidence_score=0.9
            )

        # In a real environment with a valid API key, this will call GPT-4.
        response = self.chain.invoke({
            "context": context_text,
            "test_name": failure_log.test_name,
            "error_message": failure_log.error_message,
            "traceback": failure_log.traceback
        })
        
        # Map the dictionary output back to our Pydantic domain model
        return CorrectionProposal(**response)
