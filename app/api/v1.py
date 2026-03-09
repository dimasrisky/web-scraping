from fastapi import APIRouter
from app.modules.websites.website_router import website_router

v1 = APIRouter(
    prefix='/api/v1'
)

v1.include_router(website_router)