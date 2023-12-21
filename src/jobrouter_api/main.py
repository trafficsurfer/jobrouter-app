"""FastAPI router module."""
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from . import schemas

app = FastAPI()
app.mount("/app", StaticFiles(directory="front/dist", html=True), name="static")
app.add_middleware(GZipMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=["*"])


@app.post("/suggest")
async def upload_video(resume: schemas.Resume) -> list[schemas.Job]:
    return []
