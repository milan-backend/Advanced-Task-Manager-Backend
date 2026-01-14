from datetime import datetime,timedelta

from jose import jwt,JWTError
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set")
ACCESS_TOKEN_EXPIRE_MINUTES = 15


def create_access_token(
        subject : str,
        expires_delta : timedelta | None = None,
) -> str:
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta

    else:
        expire = datetime.utcnow() + timedelta(
            minutes= ACCESS_TOKEN_EXPIRE_MINUTES
        )

    payload = {
        "sub" : subject,
        "exp" : expire,
    }


    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )



def decode_access_token(token:str) -> str:

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        subject : str | None = payload.get("sub")
        if subject is None:
            raise JWTError()
        return subject
    except JWTError:
        raise

    