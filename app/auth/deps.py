from fastapi import HTTPException,status,Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from app.auth.jwt import decode_access_token
from app.api.deps import get_db
from app.models.user import User


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl = "/auth/login"
)


def get_current_user(
        token : str = Depends(oauth2_scheme),
        db : Session = Depends(get_db),
) -> User:
    
    try:
        user_id = decode_access_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid or expire token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "User not found",
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "User account is deactivated",
            headers = {"WWW-Authenticate": "Bearer"}
        )
    

    return user
            


