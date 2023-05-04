from email.policy import default
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Boolean
from datetime import datetime
from models.base_model import BaseModel
from config.db import engine, meta

class Group(BaseModel):
    __tablename__ = "group"
    name = Column(String(255))

    description = Column(String(255))
    group_admin_id = Column(Integer, ForeignKey('user_data.id'), nullable=False)
    group_admin = relationship('User', back_populates='admin_groups')
    #members_id = ()
    #members = 
    status = Column(Boolean, default=True)
