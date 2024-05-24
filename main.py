# /usr/bin/env python3
# -*- coding: UTF-8 -*-


"""

Author: samzong.lu
E-mail: samzong.lu@gmail.com

"""

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.hello import hello

app = FastAPI(
    openapi_url="/api/v1/openapi.json",
    docs_url="/docs",
    redoc_url=None,
    title="Template Project",
    description="A template project of FastAPI",
    version="1.0",
    contact={
        "name": "Samzong Lu",
        "url": "https://samzong.me",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
    },
)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


@app.get("/hello")
async def get_hello():
    return hello()

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
