from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime
from .database import Base

class ProjectHistory(Base):
    __tablename__ = 'project_history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('project.id'))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Result fields (moved from ProjectResults)
    ca_matrix = Column(Text, nullable=True)  # CA matrix in JSON format
    cr_matrix = Column(Text, nullable=True)  # CR matrix in JSON format
    stc_value = Column(Float, nullable=True)  # STC value
    mc_stc_value = Column(Float, nullable=True)  # MC-STC value
    security_dev_emails = Column(Text, nullable=True)  # security_dev_emails
    dev_infos = Column(Text, nullable=True)  # dev_infos

    # Relationship back to Project
    project = relationship('Project', back_populates='histories')

    # Relationships to miners (moved from Project to ProjectHistory)
    assignment_matrix_miner = relationship('AssignmentMatrixMiner', back_populates='history')
    changed_files_miner = relationship('ChangedFilesMiner', back_populates='history')
    file_dependency_matrix_miner = relationship('FileDependencyMatrixMiner', back_populates='history')
