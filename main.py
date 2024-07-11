from typing import Annotated, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import SessionLocal, engine
from app.auth import check_auth
from app.settings import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@app.post("/queue/", response_model=schemas.Queue)
def create_queue(token: Annotated[str, Depends(check_auth)], queue: schemas.QueueCreate, db: Session = Depends(get_db)):
  return crud.create_queue(db=db, queue=queue)

@app.get("/queue/", response_model=list[schemas.Queue])
def read_queue(token: Annotated[str, Depends(check_auth)], skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  queue = crud.get_queues(db, skip=skip, limit=limit)
  return queue

@app.get("/queue/{queue_id}", response_model=schemas.Queue)
def read_queue(token: Annotated[str, Depends(check_auth)], queue_id: int, db: Session = Depends(get_db)):
  db_queue = crud.get_queue(db, queue_id=queue_id)
  if db_queue is None:
    raise HTTPException(status_code=404, detail="Queue not found")
  return db_queue

# TODO add pagination
@app.get("/records/")
def read_records(token: Annotated[str, Depends(check_auth)], db: Session = Depends(get_db)):
  results = crud.get_records(db)
  return results

@app.post("/records/")
@app.post("/records/{limit}")
@app.post("/records/{limit}/{verbose}")
def bulk_records(token: Annotated[str, Depends(check_auth)], limit: int = 0, verbose: Optional[bool] = False, db: Session = Depends(get_db)):
  results = crud.bulk_records(db, limit=limit, verbose=verbose)
  return results