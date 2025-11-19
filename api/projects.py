from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from typing import List, Dict, Any
from .. import database
from ..project import Project
from ..project_history import ProjectHistory
from ..assignment_matrix_miner import AssignmentMatrixMiner
from ..changed_files_miner import ChangedFilesMiner
from ..file_dependency_matrix_miner import FileDependencyMatrixMiner
import json

router = APIRouter()

@router.get("/projects/")
def get_project_list(project_name: str = Query(None), status: str = Query(None), db: Session = Depends(database.get_db)):
    query = db.query(Project)
    
    # Apply filters based on project_name and status if provided
    if project_name:
        query = query.filter(Project.name.ilike(f"%{project_name}%"))
    # if status:
    #     query = query.filter(Project.status == status)
    
    projects = query.all()
    
    # # Initialize counters for each risk level
    # high_risk_count = 0
    # mid_risk_count = 0
    # low_risk_count = 0
    
    project_list = []
    for project in projects:
        # Fetch the latest history record for the project based on mc_stc_value
        latest_project_history = db.query(ProjectHistory) \
            .filter(ProjectHistory.project_id == project.id) \
            .order_by(ProjectHistory.timestamp.desc()) \
            .first()
    
        # Check if history exists and get the latest mc_stc_value
        if latest_project_history:
            latest_mc_stc_value = latest_project_history.mc_stc_value or latest_project_history.stc_value 
    
            # Determine the risk level based on mc_stc_value
            if 0.75 < latest_mc_stc_value <= 1:
                risk_status = "low"
            elif 0.25 <= latest_mc_stc_value <= 0.75:
                risk_status = "mid"
            elif 0 <= latest_mc_stc_value < 0.25:
                risk_status = "high"
            else:
                risk_status = "undefined"
        else:
            latest_mc_stc_value = None
            risk_status = "no_project_history"
    
        # If a status filter is provided and doesn't match, skip this project
        if status and risk_status != status:
            continue
        
        # Add project data to the list
        project_list.append({
            "project_id": project.id,
            "project_name": project.name,
            "status": risk_status,
        })

    # Return the project_list in format: [{"project_id":project.id, "project_name":project.name, "status": risk_status}]
    return project_list
