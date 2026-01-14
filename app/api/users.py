from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from datetime import datetime

from app.api.deps import get_db
from app.schemas.user import UserCreate,UserRead
from app.services.user_service import create_user
from app.models.user import User
from app.auth.deps import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(
    user_in :UserCreate,
    db :Session =Depends(get_db) ,
):
    
    user = create_user(
        db=db,
        user_in = user_in,
    )

    return user


@router.get("/me", response_model = UserRead)
def read_me(
    current_user : User = Depends(get_current_user)
):
    return current_user
    

@router.delete("/me",status_code=status.HTTP_204_NO_CONTENT)
def delete_my_account(
    db :Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
):
    
    current_user.is_active = False
    current_user.deleted_at = datetime.utcnow()
    
    db.commit()