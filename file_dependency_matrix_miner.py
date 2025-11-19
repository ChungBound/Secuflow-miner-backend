import datetime
from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from .database import Base

class FileDependencyMatrixMiner(Base):
    __tablename__ = 'file_dependency_matrix_miner'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    history_id = Column(Integer, ForeignKey('project_history.id'))  # Link to ProjectHistory
    id_to_file = Column(Text, nullable=False)
    file_dependency_matrix = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    history = relationship('ProjectHistory', back_populates='file_dependency_matrix_miner')
