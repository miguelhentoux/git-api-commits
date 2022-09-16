"""Main App to run the API
"""

from fastapi import APIRouter, FastAPI

from api.api_v1 import api as v1
from api.core.config import api_settings

app = FastAPI(title="Repo API")

main_router = APIRouter()


@main_router.get("/")
def root():
    """Just a testing home page"""
    return {"message": "Hello Repos"}


app.include_router(v1.api_router, prefix=api_settings.API_V1_STR)
app.include_router(main_router)
