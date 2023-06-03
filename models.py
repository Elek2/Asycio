from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, ARRAY

from config import DSN


engine = create_async_engine(DSN)
Base = declarative_base()
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class StarPeople(Base):
    __tablename__ = "star_people"
    id = Column(Integer, primary_key=True)
    birth_year = Column(String(50))
    eye_color = Column(String(50))
    films = Column(ARRAY(String))  # Список
    gender = Column(String(50))
    hair_color = Column(String(50))
    height = Column(String(50))
    homeworld = Column(String(50))
    mass = Column(String(50))
    name = Column(String(50))
    skin_color = Column(String(50))
    species = Column(ARRAY(String))  # Список
    starships = Column(ARRAY(String))  # Список
    vehicles = Column(ARRAY(String))  # Список


