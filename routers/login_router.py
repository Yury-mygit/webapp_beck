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
    # Generate a JWT token
    token_data = {
        "sub": form_data.username,
        "exp": datetime.utcnow() + timedelta(minutes=30),
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)
    return {"access_token": token, "token_type": "bearer"}

