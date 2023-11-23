from fastapi import APIRouter, HTTPException, status, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security.oauth2 import OAuth2PasswordBearer
from pydantic import BaseModel

import jwt
from datetime import datetime, timedelta

from typing import Optional

router = APIRouter(tags=["login"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

class Token(BaseModel):
    access_token: str
    token_type: str


class UserIn(BaseModel):
    username: str
    password: str


class UserOut(UserIn):
    id: int
    is_active: bool



@router.post("/token", response_model=Token)
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    # Replace this with actual user lookup and password verification
    if form_data.username != "user" or form_data.password != "pass":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Generate JWT access token
    access_token_expires = timedelta(days=5)
    access_token_data = {
        "sub": form_data.username,
        "exp": datetime.utcnow() + access_token_expires,
    }
    access_token = jwt.encode(access_token_data, SECRET_KEY, algorithm=ALGORITHM)

    # Generate JWT refresh token
    refresh_token_expires = timedelta(days=7)
    refresh_token_data = {
        "sub": form_data.username,
        "exp": datetime.utcnow() + refresh_token_expires,
    }
    refresh_token = jwt.encode(refresh_token_data, SECRET_KEY, algorithm=ALGORITHM)

    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    response.set_cookie(key="refresh_token", value=f"Bearer {refresh_token}", httponly=True)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/token/refresh", response_model=Token)
def refresh_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    # Decode the token, allowing it to be expired up to 30 minutes
    try:
        payload = jwt.decode(form_data.username, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False})
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if datetime.utcnow() > payload["exp"] + timedelta(minutes=30):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token expired more than 30 minutes ago",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Generate a new JWT access token
    access_token_expires = timedelta(minutes=15)
    access_token_data = {
        "sub": payload["sub"],
        "exp": datetime.utcnow() + access_token_expires,
    }
    access_token = jwt.encode(access_token_data, SECRET_KEY, algorithm=ALGORITHM)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}
