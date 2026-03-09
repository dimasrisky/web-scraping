from fastapi import FastAPI
from app.api.v1 import v1
from app.core.config import config

app = FastAPI(
    title=config.PROJECT_NAME,
    summary=config.SUMMARY,
    version=config.VERSION
)

app.include_router(v1)

@app.get('/')
def root():
    return { "message": "This is root api" }