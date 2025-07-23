from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("postgresql://postgres:password@localhost/fastapi")

SessionLocal = sessionmaker(autoflush=False , autocommit=False , bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()