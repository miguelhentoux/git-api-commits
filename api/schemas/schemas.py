
"""Schemas for Response/Requests"""

from pydantic import BaseModel


class RepoResponse(BaseModel):
    """Repo/commits response model"""
    authors: list
    dates: list
    rows: list
    n_rows: int
