from sqlalchemy import Column, Integer, String
from db.database import Base 
from sqlalchemy import Column , Integer ,String


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String , nullable=False )