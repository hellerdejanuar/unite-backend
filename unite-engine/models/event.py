from email.policy import default
from operator import iconcat
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Boolean, JSON
from datetime import datetime
from models.base_model import BaseModel, Base
from models.user import attending_event_rel
from config.db import engine, meta


class Event(BaseModel): 
    __tablename__ = "event" 
    name = Column(String(255))

    event_host_id = Column(Integer, ForeignKey('user_data.id'), nullable=False) # user.id == User.id (class)
    event_host = relationship("User", back_populates="hosted_events")

    event_datetime = Column(DateTime)
    location = Column(String(255))
    description = Column(String(255))
    image_URL = Column(String(511), default="event-profile-icon.png")
    icon = Column(String(2))
    max_people = Column(Integer, default=1)
    people_count = Column(Integer, default=0)
    participants = relationship("User", primaryjoin="Event.id==attending_event_rel.c.event_id", 
                                        secondary=attending_event_rel, 
                                        back_populates='attending_events') ## related con user.id

    group_id = Column(Integer, ForeignKey('group.id'), default=None)
    channel_id = Column(Integer, ForeignKey('channel.id'), default=None)

    config = Column(JSON)
    status = Column(Boolean, default=True)

    @classmethod
    def attrs(cls, str=None):
        """ Returns a list of or attributes for the given class """
        base_attrs = BaseModel.attrs()

        public_attrs = [
                "name",
                "event_host_id",
                "event_datetime",
                "location",
                "description",
                "icon",
                "image_URL",
                "max_people",
                "people_count",
                "group_id",
                "channel_id",
                "config",
                "status"]

        rel_attrs = [
                "participants"]

        if str == None:
            return base_attrs + public_attrs
        elif str == "all":
            return base_attrs + public_attrs + rel_attrs
        elif str == "rel":
            return rel_attrs
