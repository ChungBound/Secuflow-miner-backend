from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Handle both relative and absolute imports
try:
    # Try relative imports first (for local development)
    from .. import database
    from ..models import user
except ImportError:
    # Fallback to absolute imports (for deployment)
    import database
    from models import user

router = APIRouter()

# 获取用户列表
@router.get("/users/")
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    users = db.query(user.User).offset(skip).limit(limit).all()
    return users