from fastapi import APIRouter
from fastapi import HTTPException,status,Depends,Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.user import User
from app.auth.password import verify_password
from app.auth.jwt import create_access_token
import secrets
from app.models.refresh_token import RefreshToken
from app.schemas.auth import TokenRefresh
from app.utils.rate_limiter import rate_limit
from app.schemas.common import MessageResponse



router = APIRouter(prefix="/auth",
                   tags=["auth"])

@router.post("/login")
def login(
    request : Request,
    form_data : OAuth2PasswordRequestForm = Depends(),
    db : Session = Depends(get_db),
):
    client_ip = request.client.host

    rate_limit(
        key=f"login:{client_ip}",
        limit = 5,
        window_seconds=60
    )
    


    
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user :
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid crendentials."
        )
    

    if not verify_password(
        form_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid credentials."
        )
    

    access_token = create_access_token(
        subject =str(user.id)
    )

    refresh_token_value = secrets.token_urlsafe(32)

    refresh_token = RefreshToken(
        token = refresh_token_value,
        user_id = user.id,
    )

    db.add(refresh_token)
    db.commit()

    return {
        "access_token" : access_token,
        "refresh_token" : refresh_token_value,
        "token_type" : "Bearer",
    }
    



@ router.post("/refresh")
def refresh_access_token(
    request : Request,
    token_in : TokenRefresh,
    db : Session = Depends(get_db)
):

    client_ip = request.client.host

    rate_limit(
        key=f"login:{client_ip}",
        limit = 5,
        window_seconds=60
    )
    

 
    
    refresh_token = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token == token_in.refresh_token
        ).first()
    )

    if not refresh_token or refresh_token.is_revoked:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid refresh token"
        )
    

    refresh_token.is_revoked = True

    new_refresh_token_value = secrets.token_urlsafe(32)

    new_refresh_token = RefreshToken(
        token = new_refresh_token_value,
        user_id = refresh_token.user_id,
    )

    db.add(new_refresh_token)

    access_token = create_access_token(
        subject ={"sub" : str(refresh_token.user_id)}
    )


    db.commit()


    return {
        "access_token" : access_token,
        "refresh_token" : new_refresh_token_value,
        "token_type" : "Bearer"
    }




@router.post("/logout", response_model=MessageResponse)
def logout(
    token_in : TokenRefresh,
    db : Session = Depends(get_db)
):
    
    refresh_token = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token == token_in.refresh_token)

        ).first()
    
    if not refresh_token:
        return {"detail": "Already logged out or token not found."}
    


    if refresh_token.is_revoked:
        return {"detail": "Already loggged out."}
        refresh_token.is_revoked = True

        db.commit()

    return {"detail" : "Logged out successfully"}

    