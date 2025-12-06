# ================================================================
# Orbit API
# Description: FastAPI backend for the Orbit application.
# Author: Jerry
# License: MIT
# ================================================================

# routes/test_cases.py

from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter()


class TestCase(BaseModel):
    id: str
    project_key: str
    key: str
    title: str
    description: str
    folder: str
    status: str
    priority: str
    test_scripts: str = None
    last_result: str = None
    last_execution_id: str = None
    test_frequency: list[str] = None
    labels: list[str] = None


class TestCaseCreate(BaseModel):
    key: str
    project_key: str
    title: str
    description: str
    folder: str
    status: str
    priority: str = None
    test_scripts: str = None
    last_result: str = None
    last_execution_id: str = None
    test_frequency: list[str] = None
    labels: list[str] = None


class TestCaseUpdate(BaseModel):
    title: str = None
    description: str = None
    folder: str = None
    status: str = None
    priority: str = None
    test_scripts: str = None
    last_result: str = None
    last_execution_id: str = None
    test_frequency: list[str] = None
    labels: list[str] = None


# List Test Cases
@router.get("/api/projects/{project_id}/test-cases/",
            tags=["test-cases"],
            response_model=list[TestCase])
def list_test_cases(project_id: str):
    """List all test cases in the specified project."""


# Create Test Case
@router.post("/api/projects/{project_id}/test-cases/",
             tags=["test-cases"],
             status_code=status.HTTP_204_NO_CONTENT)
def create_test_case(project_id: str,
                     test_case: TestCaseCreate):
    """Create a new test case in the specified project."""


# Delete all Test Case
@router.delete("/api/projects/{project_id}/test-cases/",
               tags=["test-cases"],
               status_code=status.HTTP_204_NO_CONTENT)
def delete_all_test_case(project_id: str):
    """Delete all test cases in the specified project."""


# Get Test Case
@router.get("/api/projects/{project_id}/test-cases/{test_case_id}",
            tags=["test-cases"],
            response_model=TestCase)
def get_test_case_by_id(project_id: str,
                        test_case_id: str):
    """Retrieve a specific test case by its ID within the specified project."""


# Update Test Case
@router.put("/api/projects/{project_id}/test-cases/{test_case_id}",
            tags=["test-cases"],
            response_model=TestCase)
def update_test_case_by_id(project_id: str,
                           test_case_id: str,
                           test_case: TestCaseUpdate):
    """Update a specific test case by its ID within the specified project."""


# Delete Test Case
@router.delete("/api/projects/{project_id}/test-cases/{test_case_id}",
               tags=["test-cases"],
               status_code=status.HTTP_204_NO_CONTENT)
def delete_test_case_by_id(project_id: str,
                           test_case_id: str):
    """Delete a specific test case by its ID within the specified project."""
