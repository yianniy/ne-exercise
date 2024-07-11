from pydantic import BaseModel, Field
from datetime import datetime

class QueueBase(BaseModel):
  timestamp: datetime
  value: float = Field(ge=0)

class QueueCreate(QueueBase):
  pass

class Queue(QueueBase):
  id: int

  class Config:
    orm_mode = True


class RecordBase(BaseModel):
  ts: datetime
  val: float = Field(ge=0)

class RecordCreate(RecordBase):
  pass

class Record(BaseModel):
  id: int
  val_sql: float
