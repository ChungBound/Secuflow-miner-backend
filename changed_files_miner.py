import datetime
from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from .database import Base

class ChangedFilesMiner(Base):
    __tablename__ = 'changed_files_miner'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    history_id = Column(Integer, ForeignKey('project_history.id'))  # Link to ProjectHistory
    id_to_file = Column(Text, nullable=False)
    id_to_user = Column(Text, nullable=False)
    changed_files_by_user = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    history = relationship('ProjectHistory', back_populates='changed_files_miner')
