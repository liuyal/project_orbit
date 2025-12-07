# ================================================================
# Orbit API
# Description: FastAPI backend for the Orbit application.
# Author: Jerry
# License: MIT
# ================================================================

# db.py

import os

from motor.motor_asyncio import AsyncIOMotorClient

from models.projects import Project
from models.test_cases import TestCase
from models.test_cycles import TestCycle
from models.test_executions import TestExecution
from orbit_def.orbit_def import (
    DB_COLLECTION_PRJ,
    DB_COLLECTION_TC,
    DB_COLLECTION_TE,
    DB_COLLECTION_TCY
)


def pydantic_to_mongo_jsonschema(pydantic_schema: dict):
    """Convert a Pydantic JSON schema to a MongoDB JSON schema."""

    type_map = {
        "string": "string",
        "integer": "int",
        "number": "double",
        "boolean": "bool"
    }

    props = {}
    required = pydantic_schema.get("required", [])
    for name, field in pydantic_schema["properties"].items():
        bson_type = type_map.get(field.get("type", "string"), "string")
        mongo_name = "_id" if name == "id" else name
        props[mongo_name] = {"bsonType": bson_type}

    return {
        "bsonType": "object",
        "required": [("_id" if r == "id" else r) for r in required],
        "properties": props
    }


project_schema = pydantic_to_mongo_jsonschema(Project.model_json_schema())
test_case_schema = pydantic_to_mongo_jsonschema(TestCase.model_json_schema())
test_execution_schema = pydantic_to_mongo_jsonschema(TestExecution.model_json_schema())
test_cycle_schema = pydantic_to_mongo_jsonschema(TestCycle.model_json_schema())

DB_COLLECTIONS = [
    (DB_COLLECTION_PRJ, project_schema),
    (DB_COLLECTION_TC, test_case_schema),
    (DB_COLLECTION_TE, test_execution_schema),
    (DB_COLLECTION_TCY, test_cycle_schema)
]

MONGODB_HOST = os.getenv("MONGODB_HOST", "localhost")
MONGODB_PORT = os.getenv("MONGODB_PORT", "27017")
MONGODB_USER = os.getenv("MONGODB_USER", "admin")
MONGODB_PASS = os.getenv("MONGODB_PASS", "password")

MONGODB_URL = f"mongodb://{MONGODB_USER}:{MONGODB_PASS}@{MONGODB_HOST}:{MONGODB_PORT}"


def get_db_client():
    """Get the MongoDB client with optional authentication."""

    return AsyncIOMotorClient(MONGODB_URL)
