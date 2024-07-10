from sqlalchemy.orm import Session
from typing import List

from . import models, schemas
from .settings import settings

from io import StringIO
import logging

def get_queue(db: Session, queue_id: int):
  return db.query(models.Queue).filter(models.Queue.id == queue_id).first()

def get_queues(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.Queue).offset(skip).limit(limit).all()

def create_queue(db: Session, queue: schemas.QueueCreate):
  db_queue = models.Queue(timestamp=queue.timestamp, value=queue.value)
  db.add(db_queue)
  db.commit()
  db.refresh(db_queue)
  return db_queue

def get_records(db: Session, skip: int = 0, limit: int = 100):
  return db.query(models.Record).offset(skip).limit(limit).all()

def create_records(db: Session, records: List[schemas.RecordCreate], verbose: bool = False):
  recordModels = []
  for record in records:
    recordModels.append(models.Record(ts=record.ts, val=record.val, val_sqr=record.val*record.val))

  db.add_all(recordModels)

  if verbose: 
    # highjack the logger and send it to a variable, thus capturing the logs that show SQL statements
    logger = logging.getLogger("sqlalchemy.engine")
    logger.setLevel(logging.INFO)
    log_capture_string = StringIO()
    ch = logging.StreamHandler(log_capture_string)
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)

    db.commit() # commit the adding of records.

    # reset the logger back to normal and capture output
    log_contents = log_capture_string.getvalue()
    logger.handlers.clear()
    log_capture_string.close()
    logger.addHandler(logging.StreamHandler())
  else:
    db.commit()
  
  for i in  range(len(recordModels)):
    db.refresh(recordModels[i])

  if verbose: 
    return {
      "records": recordModels,
      "verbose": log_contents,
      }
  else:
    return recordModels

def bulk_records(db: Session, limit: int, verbose: bool = False):
  queue = db.query(models.Queue).order_by(models.Queue.timestamp.desc()).offset(0).limit(min(limit, settings.hard_limit)).all()
  records = []

  for item in queue:
    records.append(schemas.RecordCreate(ts=item.timestamp, val=item.value))
    db.delete(item)
    db.commit()
  addedRecords = create_records(db, records, verbose)
  return addedRecords