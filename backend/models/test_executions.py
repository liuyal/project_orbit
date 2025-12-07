# ================================================================
# Orbit API
# Description: FastAPI backend for the Orbit application.
# Author: Jerry
# License: MIT
# ================================================================

# model/execution.py

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class TestExecution(BaseModel):
    _id: str
    execution_key: str
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
    execution_key: str
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
    execution_key: str
    result: str = None
    custom_fields: dict[str, str] = None
    comments: str = None
    started_at: str = None
    finished_at: str = None
    links: list[str] = None
