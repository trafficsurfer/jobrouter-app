"""Database schema for job portal app."""

from pydantic import BaseModel


class Job(BaseModel):
    """Job listing."""

    text: str


class Resume(BaseModel):
    """Resume text."""

    text: str
