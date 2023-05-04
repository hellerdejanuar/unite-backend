from datetime import datetime
from sqlalchemy import Integer, Column, String, DateTime
from config.db import meta, Base
from sqlalchemy import insert, select, update, delete, join



class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


    def to_dict(self):
        return None
        
        #return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    @classmethod
    def attrs(cls, str=None):
        attrs = ["id", "created_at", "updated_at"]
        return attrs