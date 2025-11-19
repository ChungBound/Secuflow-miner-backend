import datetime
from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from .database import Base

# Miners are now linked to ProjectHistory
class AssignmentMatrixMiner(Base):
    __tablename__ = 'assignment_matrix_miner'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    history_id = Column(Integer, ForeignKey('project_history.id'))  # Link to ProjectHistory
    id_to_file = Column(Text, nullable=False)
    assignment_matrix = Column(Text, nullable=False)
    id_to_user = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    history = relationship('ProjectHistory', back_populates='assignment_matrix_miner')
