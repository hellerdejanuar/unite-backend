from contextlib import nullcontext
from datetime import datetime, timedelta
from typing import Optional, List, Union, Any
from pydantic import BaseModel as pyBaseModel

class EventSchema(pyBaseModel):
    
    id: int 
    # created_at: datetime // inherited from BaseModel
    # updated_at: datetime // inherited from BaseModel
    name: str = "Event name"
    event_host_id: int
    event_datetime: datetime = (datetime.now() + timedelta(hours=1))
    location: str = "Location"
    description: str = "Description"
    imageURL: str = "https://i.scdn.co/image/ab6761610000e5eba317336b899ab2f39c0ede62"
    icon: str = ""
    max_people: int = 1
    people_count: int = 0 
    participants: Any = []
    group_id: Optional[int] = None 
    channel_id: Optional[int] = None
    
    config: dict = {
        "online": False
    }
