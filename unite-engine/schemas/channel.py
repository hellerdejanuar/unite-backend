from typing import Optional
from schemas.base_model import BaseModel

class ChannelSchema(BaseModel):
    name: str = ""
    channel_admin_id: int = ""
    description: str = ""
