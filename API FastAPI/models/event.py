from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Boolean, JSON
from datetime import datetime
from models.base_model import BaseModel
from config.db import engine, meta

class Event(BaseModel): 
    __tablename__ = "event" 
    name = Column(String(255))

    event_host_id = Column(Integer, ForeignKey('user_data.id'), nullable=False) # user.id == User.id (class)
    event_host = relationship("User", back_populates="hosted_events")

    event_datetime = Column(DateTime)
    location = Column(String(255))
    description = Column(String(255))
    icon = Column(String(2))
    max_people = Column(Integer, default=1)
    participants = Column(String(255)) ## related con user.id

    group_id = Column(Integer, ForeignKey('group.id'))
    channel_id = Column(Integer, ForeignKey('channel.id'))

    config = Column(JSON)
    status = Column(Boolean, default=True)

