# ================================================================
# Orbit API
# Description: FastAPI backend for the Orbit application.
# Author: Jerry
# License: MIT
# ================================================================

# tools/tools.py

from datetime import datetime, timezone

from bson import ObjectId


def convert_objectid(doc):
    """Convert ObjectId to string in a MongoDB document."""

    if doc and "_id" in doc and isinstance(doc["_id"], ObjectId):
        doc["_id"] = str(doc["_id"])

    return doc


def get_current_utc_time():
    """Get the current UTC time as an ISO formatted string."""

    current_utc_iso = datetime.now(timezone.utc).replace(microsecond=0)
    current_utc_iso = current_utc_iso.isoformat().replace("+00:00", "Z")

    return current_utc_iso
