from pydantic import BaseModel
from typing import Dict, Any, Optional

class UpdateWebsite(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    parser: Optional[Dict[str, Any]] = None
    isActive: Optional[bool] = None