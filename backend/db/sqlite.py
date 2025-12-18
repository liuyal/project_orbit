# ================================================================
# Orbit API
# Description: FastAPI backend for the Orbit application.
# Author: Jerry
# License: MIT
# ================================================================

# db/sqlitedb.py

from backend.app_def.app_def import (
    DB_NAME,
    DB_COLLECTION_PRJ,
    DB_COLLECTION_TC,
    DB_COLLECTION_TE,
    DB_COLLECTION_TCY
)
from backend.db.db import DatabaseClient, DBType, DBMode
# from backend.models.projects import Project
# from backend.models.test_cases import TestCase
# from backend.models.test_cycles import TestCycle
# from backend.models.test_executions import TestExecution

# PROJECT_SCHEMA = Project.model_json_schema()
# TEST_CASE_SCHEMA = TestCase.model_json_schema()
# TEST_EXECUTION_SCHEMA = TestExecution.model_json_schema()
# TEST_CYCLE_SCHEMA = TestCycle.model_json_schema()

DB_COLLECTIONS = [(DB_COLLECTION_PRJ, None),
                  (DB_COLLECTION_TC, None),
                  (DB_COLLECTION_TE, None),
                  (DB_COLLECTION_TCY, None)]

SQLITE_URL = f""


class SqliteClient(DatabaseClient):

    def __init__(self,
                 db_name: str = DB_NAME,
                 db_url: str = SQLITE_URL,
                 db_type: DBType = DBType.SQLITE,
                 db_mode: DBMode = DBMode.DEBUG):
        """ Initialize the Sqlite client. """

        super().__init__(db_name, db_url, db_type, db_mode)

    async def connect(self):
        """Get the client with optional authentication."""

    async def close(self):
        """ Disconnect from the database. """

    async def configure(self,
                        **kwargs) -> None:
        """Configure database connection parameters"""

    async def create(self,
                     table: str,
                     data: dict) -> bool:
        """Insert a new record into the database."""

    async def find(self,
                   table: str,
                   query: dict) -> list:
        """Retrieve records from the database."""

    async def find_one(self,
                       table: str,
                       query: dict) -> dict:
        """Retrieve a single record from the database."""

    async def update(self,
                     table: str,
                     query: dict,
                     update_data: dict) -> tuple:
        """Update records in the database."""

    async def delete(self,
                     table: str,
                     query: dict) -> tuple:
        """Delete records from the database."""

    async def delete_one(self,
                         table: str,
                         query: dict) -> tuple:
        """Delete records from the database."""

    async def execute_raw(self,
                          command,
                          *args,
                          **kwargs):
        """ Execute a raw query or command
            (SQL for SQLite, command for MongoDB).
        """
