from pydantic import BaseModel, Field
from typing import List, Optional

class FailureLog(BaseModel):
    """
    Represents a traceback or error emitted by a failed CI test pipeline.
    """
    test_name: str = Field(..., description="Name of the test that failed")
    error_message: str = Field(..., description="The high-level error message")
    traceback: str = Field(..., description="The full traceback or log of the failure")
    file_path: Optional[str] = Field(None, description="The test file where failure occurred")

class CodePatch(BaseModel):
    """
    Represents a proposed change to a file.
    """
    file_path: str = Field(..., description="The path to the file to be modified")
    action: str = Field(..., description="'modify', 'create', or 'delete'")
    old_code_snippet: Optional[str] = Field(None, description="The code that needs replacing")
    new_code_snippet: str = Field(..., description="The new code that should replace the old")

class CorrectionProposal(BaseModel):
    """
    The agent's proposed plan and code patch to fix a specific FailureLog.
    """
    failure_reason: str = Field(..., description="The agent's diagnosis of why the test failed")
    proposed_fix_description: str = Field(..., description="A high level explanation of the fix")
    patches: List[CodePatch] = Field(default_factory=list, description="The actual code patches")
    confidence_score: float = Field(..., description="Agent's confidence in this fix (0.0 to 1.0)")

class ApiDocSnippet(BaseModel):
    """
    Represents an API specification (like OpenAPI endpoint) passed down to generate tests.
    """
    endpoint_path: str = Field(..., description="The route path (e.g., /users/{id})")
    http_method: str = Field(..., description="GET, POST, PUT, DELETE, etc.")
    description: str = Field(..., description="The documentation for the endpoint")
    request_schema: Optional[dict] = Field(None, description="Expected request body")
    response_schema: Optional[dict] = Field(None, description="Expected response body")

class GenTestResponse(BaseModel):
    """
    The generated pytest code for an API spec.
    """
    test_code: str = Field(..., description="The complete python code using pytest to test the endpoint")
    test_scenarios_covered: List[str] = Field(..., description="List of scenarios generated (Happy path, Edge case, etc.)")
