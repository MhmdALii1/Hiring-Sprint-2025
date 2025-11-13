from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router

# Create the FastAPI application instance
# This is the main backend app handling all API requests
app = FastAPI(
    title="Vehicle Condition Assessment API (MVP)",
    description="Backend API for AI-powered vehicle inspection",
    version="1.0.0"
)

# Configure CORS to allow frontend applications (Ionic app) to make cross-origin requests.
# In production, this should be restricted to the frontend's domain for security.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Allow all origins for development
    allow_methods=["*"],   # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],   # Allow all headers
)

# Include API routes from routes.py
# All endpoints defined in 'router' will be available under '/api' prefix
# This modular approach keeps the app scalable and maintainable
app.include_router(router, prefix="/api")

# Root endpoint for health check
# Useful to verify that the backend is running before testing other endpoints
@app.get("/")
def root():
    return {"status": "ok", "message": "VCA backend running"}
