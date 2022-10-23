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
    icon: str = ""
    max_people: int = 1
<<<<<<< HEAD
=======
    people_count: int = 0 
>>>>>>> origin/floapp
    participants: Any = []
    group_id: Optional[int] = None 
    channel_id: Optional[int] = None
    
    config: dict = {
        "online": False
    }
