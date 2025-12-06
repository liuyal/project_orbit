# ================================================================
# Orbit API
# Description: FastAPI backend for the Orbit application.
# Author: Jerry
# License: MIT
# ================================================================

# routes/projects.py

from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter()


class Project(BaseModel):
    id: str
    key: str
    description: str
    test_cases: int
    test_cycles: int
    created_at: str
    updated_at: str = None
    is_active: bool = True


class ProjectCreate(BaseModel):
    key: str
    created_at: str
    description: str = None
    is_active: bool = None


class ProjectUpdate(BaseModel):
    description: str = None
    updated_at: str = None
    is_active: bool = None


# List Projects
@router.get("/api/projects",
            tags=["projects"],
            response_model=list[Project],
            status_code=status.HTTP_200_OK)
def list_projects():
    """Endpoint to get projects"""


# Create Project
@router.post("/api/projects",
             tags=["projects"],
             status_code=status.HTTP_204_NO_CONTENT)
def create_project(project: ProjectCreate):
    """Endpoint to create project."""


# Get Project
@router.get("/api/projects/{project_key}",
            tags=["projects"],
            response_model=Project,
            status_code=status.HTTP_200_OK)
def get_project(project_key: str):
    """Endpoint to get project"""


# Update Project
@router.put("/api/projects/{project_key}",
            tags=["projects"],
            response_model=ProjectUpdate,
            status_code=status.HTTP_200_OK)
def update_project(project_key: str,
                   project: ProjectUpdate):
    """Endpoint to update project"""


# Delete Project
@router.delete("/api/projects/{project_key}",
               tags=["projects"],
               status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_key: str):
    """Endpoint to delete project"""
