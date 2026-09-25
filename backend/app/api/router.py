from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.github import router as github_router
from app.api.repository import router as repository_router


api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(github_router)
api_router.include_router(repository_router)