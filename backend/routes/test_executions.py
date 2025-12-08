# ================================================================
# Orbit API
# Description: FastAPI backend for the Orbit application.
# Author: Jerry
# License: MIT
# ================================================================

# routes/execution.py

from fastapi import APIRouter, Request, status, Response
from starlette.responses import JSONResponse

from backend.app_def.app_def import (
    DB_COLLECTION_TE,
    DB_COLLECTION_TC
)
from backend.models.test_executions import (
    TestExecution,
    TestExecutionCreate,
    TestExecutionUpdate
)

router = APIRouter()


@router.get("/api/projects/{project_key}/test-cases/{test_case_key}/executions",
            tags=[DB_COLLECTION_TE],
            response_model=list[TestExecution])
async def get_all_executions_for_test_case(request: Request,
                                           project_key: str,
                                           test_case_key: str):
    """Get all test executions for a specific test case within a project."""

    db = request.app.state.db
    test_executions = await db.find(DB_COLLECTION_TE, {"project_key": project_key,
                                                       "test_case_key": test_case_key})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=test_executions)


@router.post("/api/projects/{project_key}/test-cases/{test_case_key}/executions",
             tags=[DB_COLLECTION_TE],
             response_model=TestExecution,
             status_code=status.HTTP_201_CREATED)
async def create_execution_for_test_case(request: Request,
                                         project_key: str,
                                         test_case_key: str,
                                         execution: TestExecutionCreate):
    """Create a new test execution for a specific test case within a project."""

    # Prepare request data
    request_data = execution.model_dump()

    # Validate test_case_key starts with project_key
    if not test_case_key.startswith(project_key):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"error": f"test_case_key {test_case_key} "
                                              f"does not start with "
                                              f"project_key {project_key}"})

    # Validate execution_key starts with project_key
    if not request_data["execution_key"].startswith(project_key):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"error": f"execution_key {request_data["execution_key"]} "
                                              f"does not start with "
                                              f"project_key {project_key}"})

    # Check if execution_key already exists
    db = request.app.state.db
    result = await db.find_one(DB_COLLECTION_TE,
                               {"execution_key": request_data["execution_key"]})
    if result is not None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"error": f"execution_key "
                                              f"{request_data["execution_key"]} "
                                              f"already exists."})

    # Initialize missing keys
    request_data["project_key"] = project_key
    request_data["test_case_key"] = test_case_key

    # Check if test_case_key exists
    result = await db.find_one(DB_COLLECTION_TC,
                               {"test_case_key": test_case_key})
    if result is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"error": f"test case "
                                              f"{test_case_key} "
                                              f"does not exists."})

    # Assign _id
    db_insert = TestExecution(**request_data).model_dump()
    db_insert["_id"] = test_case_key
    await db.create(DB_COLLECTION_TE, db_insert)

    return Response(status_code=status.HTTP_201_CREATED)


@router.delete("/api/projects/{project_key}/test-cases/{test_case_key}/executions",
               tags=[DB_COLLECTION_TE],
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_execution_for_test_case(request: Request,
                                             project_key: str,
                                             test_case_key: str):
    """Delete all test executions for a specific test case within a project."""


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
