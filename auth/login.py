from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel


class UserIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str


security = HTTPBasic()


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    # Replace this with actual user lookup
    if credentials.username != "user" or credentials.password != "pass":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return UserOut(username=credentials.username, id=1)

