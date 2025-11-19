from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime
from .database import Base

# Project Model (has multiple historical versions)
class Project(Base):
    __tablename__ = 'project'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationship to ProjectHistory
    histories = relationship('ProjectHistory', back_populates='project')
