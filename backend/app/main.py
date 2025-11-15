from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router

# -----------------------------
# FastAPI application instance
# -----------------------------
app = FastAPI(
    title="Vehicle Condition Assessment",
    description="AI-powered vehicle damage detection and cost estimation",
    version="1.0"
)

# -----------------------------
# Enable CORS for frontend
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include API routes
app.include_router(router)

# -----------------------------
# Health check endpoint
# -----------------------------
@app.get("/")
def health_check():
    """
    Simple endpoint to check API status
    """
    return {"status": "ok"}
