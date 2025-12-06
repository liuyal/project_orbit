# ================================================================
# Orbit API
# Description: FastAPI backend for the Orbit application.
# Author: Jerry
# License: MIT
# ================================================================

# routes/execution.py

from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter()


class TestExecution(BaseModel):
    id: str
    key: str
    project_key: str
    test_cycle_key: str
    test_case_key: str
    result: str
    custom_fields: dict[str, str]
    comments: str
    started_at: str
    finished_at: str
    links: list[str]


class TestExecutionCreate(BaseModel):
    key: str
    project_key: str
    test_cycle_key: str
    test_case_key: str
    result: str = None
    custom_fields: dict[str, str] = None
    comments: str = None
    started_at: str = None
    finished_at: str = None
    links: list[str] = None


class TestExecutionUpdate(BaseModel):
    key: str
    result: str = None
    custom_fields: dict[str, str] = None
    comments: str = None
    started_at: str = None
    finished_at: str = None
    links: list[str] = None


# List Executions For Test Case
@router.get("/api/projects/{project_id}/test-cases/{test_case_id}/executions",
            tags=["executions"],
            response_model=list[TestExecution])
def list_executions_for_test_case(project_id: str,
                                  test_case_id: str):
    return


# Create Execution For Test Case
@router.post("/api/projects/{project_id}/test-cases/{test_case_id}/executions",
             tags=["executions"],
             response_model=TestExecution,
             status_code=status.HTTP_201_CREATED)
def create_execution_for_test_case(project_id: str,
                                   test_case_id: str):
    return


# Get Execution
@router.get("/api/executions/{execution_id}",
            tags=["executions"],
            response_model=TestExecution)
def get_execution(execution_id: str):
    return


# Update Execution
@router.put("/api/executions/{execution_id}",
            tags=["executions"],
            response_model=TestExecutionUpdate)
def update_execution(execution_id: str):
    return


# Delete Execution
@router.delete("/api/executions/{execution_id}",
               tags=["executions"],
               status_code=status.HTTP_204_NO_CONTENT)
def delete_execution(xecution_id: str):
    return
