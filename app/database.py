from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# TODO update db engine creation so that logging is off (i.e. echo=False) in production env
engine = create_engine(
  SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True, hide_parameters=False
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()