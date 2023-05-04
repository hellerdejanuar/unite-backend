from socket import AI_NUMERICHOST
from typing import Any, Union
from datetime import datetime
from schemas.base_model import BaseModel

class UserSchemaCreation(BaseModel):
    id: int
    name: str = ""
    email: str = ""
    password: str = ""
    phone: str = ""
    created_at: Any
    updated_at: Any

class UserSchema(BaseModel):
    id: int
    name: str = ""
    email: str = ""
    password: str = ""
    image_URL: str = ""
    phone: str = ""
    created_at: Any
    updated_at: Any

class UserSchemaDetail(BaseModel):
    id: int
    name: str = ""
    email: str = ""
    password: str = ""
    phone: str = ""
    created_at: Any
    updated_at: Any
    hosted_events: Any
    admin_groups: Any
    admin_channels: Any
    contacts: Any
    in_contacts_of: Any


