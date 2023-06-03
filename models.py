from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Text, create_engine

from config import DSN


engine = create_engine(DSN)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class StarPeople(Base):
    __tablename__ = "star_people"
    id = Column(Integer, primary_key=True)
    birth_year = Column(String(50))
    eye_color = Column(String(50))
    films = Column(Text())  # Список
    gender = Column(String(50))
    hair_color = Column(String(50))
    height = Column(String(50))
    homeworld = Column(String(50))
    mass = Column(String(50))
    name = Column(String(50))
    skin_color = Column(String(50))
    species = Column(Text())  # Список
    starships = Column(Text())  # Список
    vehicles = Column(Text())  # Список


Base.metadata.create_all(engine)
