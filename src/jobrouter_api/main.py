"""FastAPI router module."""
import os
from fastapi import Depends, FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from . import schemas, models

QDRANT_URL = os.environ['QDRANT_URL']
QDRANT_KEY = os.environ['QDRANT_KEY']

app = FastAPI()
app.mount("/app", StaticFiles(directory="front/dist", html=True), name="static")
app.add_middleware(GZipMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=["*"],allow_methods=["GET", "POST"])

qdrant_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_KEY)

model_name = 'intfloat/multilingual-e5-large'
model = SentenceTransformer(model_name)


SQLALCHEMY_DATABASE_URL = "sqlite:///./jobs.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/suggest", response_model=list[schemas.Job])
async def get_matching_jobs(resume: schemas.Resume, db=Depends(get_db)):
    query_embedding = model.encode(resume.text, convert_to_tensor=True).tolist()

    hits = qdrant_client.search(
        collection_name="vc_vectors",
        query_vector=query_embedding,
        limit=10,
    )
    ids = [job.id for job in hits]
    texts = db.query(models.Job).filter(models.Job.id.in_(ids)).all()
    return texts

@app.post('/jobs')
async def add_jobs(jobs: list[str], db=Depends(get_db)):
    for id, text in enumerate(jobs):
        row = models.Job(text=text, id=id)
        db.add(row)
    db.commit()
    return {}