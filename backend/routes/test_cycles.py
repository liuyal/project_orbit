# ================================================================
# Orbit API
# Description: FastAPI backend for the Orbit application.
# Author: Jerry
# License: MIT
# ================================================================

# routes/cycles.py

from fastapi import APIRouter, Request, status, Response
from starlette.responses import JSONResponse

from backend.app_def.app_def import (
    DB_COLLECTION_PRJ,
    DB_COLLECTION_TCY
)
from backend.models.test_cycles import (
    TestCycle,
    TestCycleCreate,
    TestCycleUpdate

)
from backend.routes.test_executions import TestExecution
from backend.tools.tools import get_current_utc_time

router = APIRouter()


@router.get("/tm/api/v1/projects/{project_key}/cycles",
            tags=[DB_COLLECTION_TCY],
            response_model=list[TestCycle])
async def get_all_cycles_for_project(request: Request,
                                     project_key: str):
    """Get all test cycles for project."""

    # Retrieve all test cycles from the database matching project_key
    db = request.app.state.db
    test_cycles = await db.find(DB_COLLECTION_TCY,
                                {"project_key": project_key})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=test_cycles)


@router.post("/tm/api/v1/projects/{project_key}/cycles",
             tags=[DB_COLLECTION_TCY],
             response_model=TestCycle,
             status_code=status.HTTP_201_CREATED)
async def create_cycle_for_project(request: Request,
                                   project_key: str,
                                   cycle: TestCycleCreate):
    """Create a new test cycle for project."""

    current_time = get_current_utc_time()

    # Prepare request data
    request_data = cycle.model_dump()

    # Retrieve all test cycles from the database matching project_key
    db = request.app.state.db

    # Validate that test_case_key starts with project_key
    if not request_data["test_cycle_key"].startswith(project_key):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"error": f"Mismatch test_cycle_key "
                                              f"{request_data["test_cycle_key"]} "
                                              f"with project_key {project_key}"})

    # Check if test_case_key already exists
    result = await db.find_one(DB_COLLECTION_TCY,
                               {"test_cycle_key": request_data["test_cycle_key"]})
    if result is not None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"error": f"test cycle "
                                              f"{request_data['test_cycle_key']} "
                                              f"already exists."})

    # Check if project_key exists
    result = await db.find_one(DB_COLLECTION_PRJ,
                               {"project_key": project_key})
    if result is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"error": f"Project {project_key} "
                                              f"not found."})

    # Initialize counts and timestamps
    request_data["project_key"] = project_key
    request_data["created_at"] = current_time
    request_data["updated_at"] = current_time

    # Assign _id
    db_insert = TestCycle(**request_data).model_dump()
    db_insert["_id"] = request_data["test_cycle_key"]
    await db.create(DB_COLLECTION_TCY, db_insert)

    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/tm/api/v1/cycles/{test_cycle_key}",
            tags=[DB_COLLECTION_TCY],
            response_model=TestCycle)
async def get_cycle_by_id(request: Request,
                          test_cycle_key: str):
    """Get a specific test cycle by its ID."""

    # Retrieve the test cycle from the database
    db = request.app.state.db
    result = await db.find_one(DB_COLLECTION_TCY,
                               {"test_cycle_key": test_cycle_key})

    if result is None:
        # test case not found
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"error": f"Test cycle "
                                              f"{test_cycle_key} "
                                              f"not found."})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=result)


@router.put("/tm/api/v1/cycles/{test_cycle_key}",
            tags=[DB_COLLECTION_TCY],
            response_model=TestCycle)
async def update_cycle_by_id(request: Request,
                             test_cycle_key: str,
                             cycle: TestCycleUpdate):
    """Update a specific test cycle by its ID."""

    current_time = get_current_utc_time()

    # Prepare request data, excluding None values
    request_data = cycle.model_dump()
    request_data = {k: v for k, v in request_data.items() if v is not None}
    request_data["updated_at"] = current_time

    # Update the cycle in the database
    db = request.app.state.db
    result, matched_count = await db.update(DB_COLLECTION_TCY,
                                            {"test_cycle_key": test_cycle_key},
                                            request_data)
    if matched_count == 0:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"error": f"Test cycle "
                                              f"{test_cycle_key} "
                                              f"not found."})

    # Retrieve the updated test case
    updated_test_cycle = await db.find_one(DB_COLLECTION_TCY,
                                          {"test_cycle_key": test_cycle_key})

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=updated_test_cycle)

@router.delete("/tm/api/v1/cycles/{test_cycle_key}",
               tags=[DB_COLLECTION_TCY],
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_cycle_by_id(request: Request,
                             test_cycle_key: str):
    """Delete a specific test cycle by its ID."""

    # Delete the test_cycle from the database
    db = request.app.state.db
    result, deleted_count = await db.delete_one(DB_COLLECTION_TCY,
                                                {"test_cycle_key": test_cycle_key})
    if deleted_count == 0:
        # Test case not found
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"error": f"Test cycle "
                                              f"{test_cycle_key} "
                                              f"not found."})

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/tm/api/v1/cycles/{test_cycle_key}/executions",
            tags=[DB_COLLECTION_TCY],
            response_model=list[TestExecution])
async def get_cycle_executions(request: Request,
                               test_cycle_key: str):
    """Get all test executions associated with a specific test cycle."""


@router.post("/tm/api/v1/cycles/{test_cycle_key}/executions",
             tags=[DB_COLLECTION_TCY],
             status_code=status.HTTP_204_NO_CONTENT)
async def add_execution_to_cycle(request: Request,
                                 test_cycle_key: str,
                                 execution_key: str):
    """Add a test execution to a specific test cycle."""


@router.delete("/tm/api/v1/cycles/{test_cycle_key}/executions/{execution_id}",
               tags=[DB_COLLECTION_TCY],
               status_code=status.HTTP_204_NO_CONTENT)
async def remove_executions_from_cycle(request: Request,
                                       test_cycle_key: str,
                                       execution_id: str):
    """Remove all test executions from a specific test cycle."""
