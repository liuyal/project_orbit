# ================================================================
# Orbit API
# Description: FastAPI backend for the Orbit application.
# Version: 0.1.0
# Author: Jerry
# License: MIT
# ================================================================

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from routes import routers

app = FastAPI(title="ORBIT",
              description="API spec for Orbit application",
              version="0.1.0",
              debug=True)


@app.get("/", tags=["root"])
def root():
    """ Root endpoint to check service status. """

    # TODO add service status info

    # redirect to /docs for now
    return RedirectResponse(url="/docs")


for router in routers:
    app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5080)
