from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    description="Backend API for DevPilot AI",
    version=settings.app_version,
)

@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.app_name} 🚀"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "application": settings.app_name,
        "version": settings.app_version,
    }