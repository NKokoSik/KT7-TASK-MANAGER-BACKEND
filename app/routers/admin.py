from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies import require_admin
from app.models.user import User
from app.schemas.auth import UserRead

router = APIRouter(prefix="/admin", tags=["administration"])

@router.get("/users", response_model=list[UserRead])
def all_users(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    return db.query(User).order_by(User.id).all()
