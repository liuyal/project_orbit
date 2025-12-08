# ================================================================
# Orbit API
# Description: FastAPI backend for the Orbit application.
# Version: 0.1.0
# Author: Jerry
# License: MIT
# ================================================================

import argparse
import logging.config
import os
import pathlib
from contextlib import asynccontextmanager

import uvicorn
import yaml
from fastapi import FastAPI

from backend.db.db import DBType
from db.mongodb import MongoClient
from db.sqlite import SqliteClient
from routes import routers

logger = logging.getLogger(__name__)


def build_parser():
    """ Build argument parser. """

    parser = argparse.ArgumentParser(
        description='Orbit FastAPI Backend'
    )
    parser.add_argument(
        '--host',
        dest='host',
        default='127.0.0.1',
        help='Set server host (default:127.0.0.1)'
    )
    parser.add_argument(
        '-p', '--port',
        dest='port',
        default=8000,
        help='Set server listening port (default: 8000)'
    )
    parser.add_argument(
        '--db',
        dest='db_type',
        type=lambda x: DBType(x),
        choices=[DBType.MONGODB, DBType.SQLITE],
        default=DBType.MONGODB,
        help='Set database type, choices: mongodb, sqlite. (default: mongodb)'
    )
    parser.add_argument(
        '--debug',
        dest='debug',
        action='store_true',
        help='Set server to debug'
    )
    return parser


@asynccontextmanager
async def lifespan(app):
    """ Lifespan context manager to handle startup and shutdown events. """

    if args.db_type == DBType.MONGODB:
        client = MongoClient()

    else:
        client = SqliteClient()

    await client.connect()
    await client.configure()

    # Attach the database client to the app state
    app.state.db = client
    yield
    await client.close()


def configure_logging_file(debug: bool = False) -> str:
    """ Configure logging from file. """

    tmp_path = os.getenv("TEMP", str(pathlib.Path(__file__).parent / 'tmp'))
    tmp_path = pathlib.Path(tmp_path)

    with open(pathlib.Path(__file__).parent / 'log_conf.yaml', 'r') as f:
        conf_text = f.read()
        if debug:
            conf_text = conf_text.replace('<LEVEL>', "DEBUG")

        else:
            conf_text = conf_text.replace('<LEVEL>', "INFO")

        log_conf_text = yaml.safe_load(conf_text)

    log_conf_path = tmp_path / 'log_conf.yaml'
    with open(log_conf_path, 'w') as f:
        yaml.dump(log_conf_text, f)

    return str(log_conf_path)


parser = build_parser()
args = parser.parse_args()

app = FastAPI(title="ORBIT",
              description="API spec for Orbit application",
              version="0.1.0",
              debug=args.debug,
              lifespan=lifespan)

for router in routers:
    app.include_router(router)

if __name__ == "__main__":
    log_conf = configure_logging_file(args.debug)
    uvicorn.run("index:app",
                host=args.host,
                port=args.port,
                reload=False,  # args.debug,
                log_config=log_conf)
