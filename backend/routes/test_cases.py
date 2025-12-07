# ================================================================
# Orbit API
# Description: FastAPI backend for the Orbit application.
# Author: Jerry
# License: MIT
# ================================================================

# routes/test_cases.py

from fastapi import APIRouter, Request, status
from starlette.responses import JSONResponse

from backend.orbit_def.orbit_def import DB_COLLECTION_TC
from backend.models.test_cases import TestCase, TestCaseCreate, TestCaseUpdate
from backend.tools.utility import (
    convert_objectid
)

router = APIRouter()


@router.get("/api/projects/{project_key}/test-cases/",
            tags=[DB_COLLECTION_TC],
            response_model=list[TestCase])
async def list_test_cases(request: Request,
                          project_key: str):
    """List all test cases in the specified project."""

    db = request.app.state.db
    projects_cursor = db[DB_COLLECTION_TC].find({})
    projects = await projects_cursor.to_list()
    projects = [convert_objectid(p) for p in projects]

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=projects)


@router.post("/api/projects/{project_key}/test-cases/",
             tags=[DB_COLLECTION_TC],
             status_code=status.HTTP_204_NO_CONTENT)
async def create_test_case(request: Request,
                           project_key: str,
                           test_case: TestCaseCreate):
    """Create a new test case in the specified project."""


@router.delete("/api/projects/{project_key}/test-cases/",
               tags=[DB_COLLECTION_TC],
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_test_case(request: Request,
                               project_key: str):
    """Delete all test cases in the specified project."""


@router.get("/api/projects/{project_key}/test-cases/{test_case_key}",
            tags=[DB_COLLECTION_TC],
            response_model=TestCase)
async def get_test_case_by_key(request: Request,
                               project_key: str
                               , test_case_key: str):
    """Retrieve a specific test case by its ID within the specified project."""


@router.put("/api/projects/{project_key}/test-cases/{test_case_key}",
            tags=[DB_COLLECTION_TC],
            response_model=TestCase)
async def update_test_case_by_key(request: Request,
                                  project_key: str,
                                  test_case_key: str,
                                  test_case: TestCaseUpdate):
    """Update a specific test case by its ID within the specified project."""


@router.delete("/api/projects/{project_key}/test-cases/{test_case_key}",
               tags=[DB_COLLECTION_TC],
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_test_case_by_key(request: Request,
                                  project_key: str,
                                  test_case_key: str):
    """Delete a specific test case by its ID within the specified project."""
