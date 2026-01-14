from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.schemas.user import UserCreate
from app.auth.password import hash_password


def create_user(db :Session, user_in :UserCreate) -> User:

    existing_user = db.query(User).filter(User.email == user_in.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = "Email already registered."
        )
    
    hashed_password = hash_password(user_in.password)

    user = User(
        email = user_in.email,
        hashed_password = hashed_password,
    )

    db.add(user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail = "Email already registered."
        )
    
    db.refresh(user)

    return user