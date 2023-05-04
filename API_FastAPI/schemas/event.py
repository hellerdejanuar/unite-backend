from contextlib import nullcontext
from datetime import datetime, timedelta
from typing import Optional, List, Union, Any
from schemas.base_model import BaseModel

class EventSchema(BaseModel):
    
    id: int 
    # created_at: datetime // inherited from BaseModel
    # updated_at: datetime // inherited from BaseModel
    name: str = "Event name"
    event_host_id: int
    event_datetime: datetime = (datetime.now() + timedelta(hours=1))
    location: str = "Location"
    description: str = "Description"
    image_URL: Optional[str] 
    icon: str = ""
    max_people: int = 1
    people_count: int = 0 
    participants: Any = []
    group_id: Optional[int] = None 
    channel_id: Optional[int] = None
    
    config: dict = {
        "online": False
    }