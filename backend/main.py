"""
Entry point for the FastAPI backend.

Responsibilities:
    - Set up CORS for frontend communication
    - Serve original fashion images as static files
    - Register all API routes from the routes module
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api.routes import router

# Initialize FastAPI app
app = FastAPI()

# Enable CORS to allow frontend to access backend endpoints
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static file directory to serve images directly via /fw25/{path}
# This assumes original runway images are stored in the "fw25" directory
app.mount(
    "/fw25",
    StaticFiles(directory=os.path.abspath("fw25")),
    name="images"
)

# Register routes from external router module
app.include_router(router)
