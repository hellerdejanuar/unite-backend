from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Boolean
from datetime import datetime
from models.base_model import BaseModel

class Channel(BaseModel):
    __tablename__ = "channel"
    name = Column(String(255))

    description = Column(String(255))
    channel_admin_id = Column(Integer, ForeignKey('user_data.id'), nullable=False)
    status = Column(Boolean, default=True)

    # Relations --
    channel_admin = relationship('User', back_populates='admin_channels')
