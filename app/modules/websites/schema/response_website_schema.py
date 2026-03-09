from .create_website_schema import CreateWebsite
from typing import Dict, Any
from pydantic import BaseModel

class ResponseWebsite(BaseModel):
    id: int
    name: str
    url: str
    parser: Dict[str, Any]
    is_active: bool

    class Config:
        from_attributes = True

class ResponseDetailWebsite(BaseModel):
    data: ResponseWebsite

class ResponseListWebsite(BaseModel):
    data: list[ResponseWebsite]