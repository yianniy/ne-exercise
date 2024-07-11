from sqlalchemy import Column, Integer, DateTime, Float
from sqlalchemy.orm import relationship

from .database import Base

class Queue(Base):
  __tablename__ = "queue"

  id = Column(Integer, primary_key=True)
  timestamp = Column(DateTime, unique=False, index=True)
  value = Column(Float)

class Record(Base):
  __tablename__ = "records"

  id = Column(Integer, primary_key=True)
  ts = Column(DateTime, unique=False, index=True)
  val = Column(Float)
  val_sqr = Column(Float)