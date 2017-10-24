from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import relationship

from . import settings

def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))

DeclarativeBase = declarative_base()

class Performance(DeclarativeBase):
    __tablename__ = "performance"
    peal_id = Column(Integer, ForeignKey('performances.id'), primary_key=True)
    ring_id = Column(Integer, ForeignKey('ringers.id'), primary_key=True)
    conductor = Column(Boolean)
    bell = Column(String)
    ringer = relationship("Ringer", back_populates="peals")
    peal = relationship("Peal", back_populates="ringers")
)
class Peal(DeclarativeBase):
    """Sqlalchemy Peals model"""
    __tablename__ = "performances"

    id = Column(Integer, primary_key=True)
    association = Column(String)
    place = Column(String, nullable=True)
    address = Column(String, nullable=True)
    changes = Column(Integer)
    name = Column(String)
    date = Column(String, nullable=True)
    footnote = Column(String) 
    donation = Column(String)
    ringers = relationship("Performance", back_populates="peals")
    page_data = Column(String)
    spider_source = Column(String)
    original_url = Column(String)
    conductor_known = Column(Boolean)

class Ringer(DeclarativeBase):
    __tablename__ = "ringers"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, unique=True)
    peals = relationship("Performance", back_populates="ringers")

def create_tables(engine):
    """
    Create tables for the models
    """
    DeclarativeBase.metadata.create_all(engine)
