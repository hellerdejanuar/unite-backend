from typing import Optional
from schemas.base_model import BaseModel

class GroupSchema(BaseModel):
    name: str = ""
    group_admin_id: int = ""
    description: str = ""