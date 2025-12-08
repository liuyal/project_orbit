# ================================================================
# Orbit API
# Description: FastAPI backend for the Orbit application.
# Author: Jerry
# License: MIT
# ================================================================

# routes/execution.py

from fastapi import APIRouter, Request, status

from backend.models.test_executions import TestExecution, TestExecutionCreate, TestExecutionUpdate
from backend.orbit_def.orbit_def import DB_COLLECTION_TE

router = APIRouter()


@router.get("/api/projects/{project_key}/test-cases/{test_case_key}/executions",
            tags=[DB_COLLECTION_TE],
            response_model=list[TestExecution])
async def get_all_executions_for_test_case(request: Request,
                                           project_key: str,
                                           test_case_key: str):
    """Get all test executions for a specific test case within a project."""


@router.post("/api/projects/{project_key}/test-cases/{test_case_key}/executions",
             tags=[DB_COLLECTION_TE],
             response_model=TestExecution,
             status_code=status.HTTP_201_CREATED)
async def create_execution_for_test_case(request: Request,
                                         project_key: str,
                                         test_case_key: str,
                                         execution: TestExecutionCreate):
    """Create a new test execution for a specific test case within a project."""


@router.get("/api/executions/{execution_key}",
            tags=[DB_COLLECTION_TE],
            response_model=TestExecution)
async def get_execution(request: Request,
                        execution_key: str):
    """Retrieve a specific test execution by its ID."""


@router.put("/api/executions/{execution_key}",
            tags=[DB_COLLECTION_TE],
            response_model=TestExecutionUpdate)
async def update_execution(request: Request,
                           execution_key: str,
                           execution: TestExecutionUpdate):
    """Update a specific test execution by its ID."""


@router.delete("/api/executions/{execution_key}",
               tags=[DB_COLLECTION_TE],
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_execution(request: Request,
                           execution_key: str):
    """Delete a specific test execution by its ID."""
