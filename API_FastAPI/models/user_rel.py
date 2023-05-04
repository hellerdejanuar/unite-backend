from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Boolean
from models.base_model import BaseModel, Base

attending_event_rel = Table(
    "attending_event_rel",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user_data.id"), primary_key=True),
    Column("event_id", Integer, ForeignKey("event.id"), primary_key=True),
)


contact_rel = Table(
    "contact_rel",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user_data.id"), primary_key=True),
    Column("contact_id", Integer, ForeignKey("user_data.id"), primary_key=True)
)

friendship_rel = Table(
    "friendship_rel",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user_data.id"), primary_key=True),
    Column("friend_id", Integer, ForeignKey("user_data.id"), primary_key=True),
)