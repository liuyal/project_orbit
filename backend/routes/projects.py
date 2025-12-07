# ================================================================
# Orbit API
# Description: FastAPI backend for the Orbit application.
# Author: Jerry
# License: MIT
# ================================================================

# routes/projects.py

from fastapi import APIRouter, Request, status, Response
from pydantic import BaseModel
from starlette.responses import JSONResponse

from .utility import (
    convert_objectid,
    get_current_utc_time
)

router = APIRouter()


class Project(BaseModel):
    _id: str
    project_key: str
    description: str
    test_case_count: int
    test_execution_count: int
    test_cycle_count: int
    created_at: str
    updated_at: str
    is_active: bool
    model_config = {"extra": "forbid"}


class ProjectCreate(BaseModel):
    project_key: str
    description: str = ""
    is_active: bool = True
    model_config = {"extra": "forbid"}


class ProjectUpdate(BaseModel):
    description: str = None
    is_active: bool = None
    model_config = {"extra": "forbid"}


@router.get("/api/projects",
            tags=["projects"],
            response_model=list[Project],
            status_code=status.HTTP_200_OK)
async def list_projects(request: Request):
    """Endpoint to get projects"""

    db = request.app.state.db
    projects_cursor = db["projects"].find({})
    projects = await projects_cursor.to_list()
    projects = [convert_objectid(p) for p in projects]

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=projects)


@router.post("/api/projects",
             tags=["projects"],
             status_code=status.HTTP_201_CREATED)
async def create_project(request: Request,
                         project: ProjectCreate):
    """Endpoint to create project."""

    current_time = get_current_utc_time()

    request_data = project.model_dump()

    db = request.app.state.db
    result = await db["projects"].find_one(
        {"project_key": request_data["project_key"]})

    if result is not None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"error": f"Project {request_data['project_key']} "
                                              f"already exists."})

    request_data["test_case_count"] = 0
    request_data["test_execution_count"] = 0
    request_data["test_cycle_count"] = 0
    request_data["created_at"] = current_time
    request_data["updated_at"] = current_time

    await db["projects"].insert_one(Project(**request_data).model_dump())

    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/api/projects/{project_key}",
            tags=["projects"],
            response_model=Project,
            status_code=status.HTTP_200_OK)
async def get_project(request: Request,
                      project_key: str):
    """Endpoint to get project"""

    db = request.app.state.db
    result = await db["projects"].find_one({"project_key": project_key})

    if result is None:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"error": f"Project {project_key} not found."})
    else:
        result = convert_objectid(result)
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=result)


@router.put("/api/projects/{project_key}",
            tags=["projects"],
            response_model=Project,
            status_code=status.HTTP_200_OK)
async def update_project(request: Request,
                         project_key: str,
                         project_update: ProjectUpdate):
    """Endpoint to update project"""

    current_time = get_current_utc_time()

    request_data = project_update.model_dump()
    request_data = {k: v for k, v in request_data.items() if v is not None}
    request_data["updated_at"] = current_time

    db = request.app.state.db

    result = await db["projects"].update_one(
        {"project_key": project_key},
        {"$set": request_data})

    if result.matched_count == 0:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"error": f"Project {project_key} not found."})

    updated_project = await db["projects"].find_one({"project_key": project_key})
    updated_project = convert_objectid(updated_project)

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=updated_project)


@router.delete("/api/projects/{project_key}",
               tags=["projects"],
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(request: Request,
                         project_key: str):
    """Endpoint to delete project"""

    db = request.app.state.db
    result = await db["projects"].delete_one({"project_key": project_key})

    if result.deleted_count == 0:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"error": f"Project {project_key} not found."})

    return Response(status_code=status.HTTP_204_NO_CONTENT)
