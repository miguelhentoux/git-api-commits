"""Router to v1
"""

from fastapi import APIRouter

from api.api_v1.endpoints import repo

api_router = APIRouter()
api_router.include_router(repo.api_router, prefix="/repo", tags=["repo"])
