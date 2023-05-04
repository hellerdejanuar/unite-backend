from pydantic import BaseModel as pyBaseModel

class BaseModel(pyBaseModel):
  class Config:
    orm_mode = True