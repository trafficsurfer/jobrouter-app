"""FastAPI router module."""
import os
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

from . import schemas

QDRANT_URL = os.environ['QDRANT_URL']
QDRANT_KEY = os.environ['QDRANT_KEY']

app = FastAPI()
app.mount("/app", StaticFiles(directory="front/dist", html=True), name="static")
app.add_middleware(GZipMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=["*"],allow_methods=["GET", "POST"])

qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_KEY)

model_name = 'intfloat/multilingual-e5-large'
model = SentenceTransformer(model_name)

@app.post("/suggest")
async def get_matching_jobs(resume: schemas.Resume) -> list[schemas.Job]:
    query_embedding = model.encode(resume.text, convert_to_tensor=True).tolist()

    hits = qdrant_client.search(
        collection_name="vc_vectors",
        query_vector=query_embedding,
        limit=10,
    )
    return [schemas.Job(text=job.payload['title']) for job in hits]
