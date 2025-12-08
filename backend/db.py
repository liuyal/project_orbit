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
    """Convert a Pydantic JSON schema to a MongoDB JSON schema, supporting Optionals (| None)."""

    def is_required(field_name):
        """ Only non-optional fields should be required """

        field = pydantic_schema["properties"][field_name]
        if "anyOf" in field:
            for option in field["anyOf"]:
                if option.get("type") == "null":
                    return False

        if field.get("nullable"):
            return False

        return True

    type_map = {
        "string": "string",
        "integer": "int",
        "number": "double",
        "boolean": "bool"
    }

    props = {}
    required = pydantic_schema.get("required", [])
    for name, field in pydantic_schema["properties"].items():
        # Determine bsonType(s)
        bson_types = set()

        # Handle Pydantic's 'anyOf' for Optionals
        if "anyOf" in field:
            for option in field["anyOf"]:
                if option.get("type") == "null":
                    bson_types.add("null")

                elif option.get("type") == "array" and option.get("items", {}).get("type") == "string":
                    bson_types.add("array:string")

                elif option.get("type"):
                    bson_types.add(type_map.get(option["type"], option["type"]))
        else:
            # Handle 'nullable' (Pydantic 2+)
            if field.get("nullable"):
                bson_types.add("null")

            if field.get("type") == "array" and field.get("items", {}).get("type") == "string":
                bson_types.add("array:string")

            elif field.get("type"):
                bson_types.add(type_map.get(field["type"], field["type"]))

        # Convert array:string to MongoDB array of string
        if "array:string" in bson_types:
            bson_types.discard("array:string")
            arr_schema = {"bsonType": "array", "items": {"bsonType": "string"}}

            if bson_types:
                # e.g. array of string or null
                anyof_list = [arr_schema] + [{"bsonType": t} for t in bson_types if t != "null"]
                if "null" in bson_types:
                    anyof_list.append({"bsonType": "null"})

                arr_schema = {"anyOf": anyof_list}
                props["_id" if name == "id" else name] = arr_schema

            else:
                props["_id" if name == "id" else name] = arr_schema

        else:
            # If multiple types, use a list
            if len(bson_types) > 1:
                props["_id" if name == "id" else name] = {"bsonType": list(bson_types)}

            elif len(bson_types) == 1:
                props["_id" if name == "id" else name] = {"bsonType": list(bson_types)[0]}

            else:
                props["_id" if name == "id" else name] = {"bsonType": "string"}

    required_fields = ["_id" if r == "id" else r for r in required if is_required(r)]

    return {
        "bsonType": "object",
        "required": required_fields,
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
