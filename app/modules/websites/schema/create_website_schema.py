from pydantic import BaseModel
from typing import Dict, Any

class CreateWebsite(BaseModel):
    name: str
    url: str
    parser: Dict[str, Any]
    isActive: bool