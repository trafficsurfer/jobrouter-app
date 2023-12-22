"""Database schema for job portal app."""

from pydantic import BaseModel


class Job(BaseModel):
    """Job listing."""

    text: str

    class Config:
        from_attributes = True

class UploadJob(BaseModel):
    """Job listing for publish"""
    
    id: int
    text: str


class Resume(BaseModel):
    """Resume text."""

    text: str
