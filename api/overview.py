from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import database
from ..project import Project
from ..project_history import ProjectHistory



router = APIRouter()

# Get project risk information
@router.get("/overview/")
def get_project_risk_overview(db: Session = Depends(database.get_db)):        
    # Use the coalesce function, when mc_stc_value is null, use stc_value
    risk_value = func.coalesce(ProjectHistory.mc_stc_value, ProjectHistory.stc_value)

    # Query the number of low-risk projects: MC-STC between (0.75, 1]
    low_risk_count = db.query(ProjectHistory).filter(risk_value > 0.75, risk_value <= 1).count()
    
    # Query the number of medium-risk projects: MC-STC between [0.25, 0.75]
    mid_risk_count = db.query(ProjectHistory).filter(risk_value >= 0.25, risk_value <= 0.75).count()
    
    # Query the number of high-risk projects: MC-STC between [0, 0.25)
    high_risk_count = db.query(ProjectHistory).filter(risk_value >= 0, risk_value < 0.25).count()
    
    # Query the total number of projects
    total_risk_count = db.query(ProjectHistory).count()

    # Return an overview of project risk information
    return {
        "highRiskCount": high_risk_count,
        "midRiskCount": mid_risk_count,
        "lowRiskCount": low_risk_count,
        "totalRiskCount": total_risk_count
    }
