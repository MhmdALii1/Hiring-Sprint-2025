# backend/app/main.py
"""
Entrypoint for the Vehicle Condition Assessment (VCA) backend.
Creates the FastAPI app, configures CORS, and includes API routes.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router

app = FastAPI(
    title="Vehicle Condition Assessment API (MVP)",
    description="Backend API for AI-powered vehicle inspection",
    version="1.0.0",
)

# Allow frontend to call this API during development.
# In production restrict allow_origins to the frontend domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the routes under /api to keep URLs organized
app.include_router(router, prefix="/api")


@app.get("/")
def root():
    """Health check endpoint (useful for monitoring / smoke tests)."""
    return {"status": "ok", "message": "VCA backend running"}
