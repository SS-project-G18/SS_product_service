


import os
from datetime import datetime, timedelta
from typing import Union
from uuid import uuid4

import jwt
# from config import ALGORITHM
from db.user import get_user_with_id
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token" )


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.environ.get("JWT_SECRET"), algorithm="HS256")
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.environ.get("JWT_SECRET"), algorithms=["HS256"])
        username: str = payload.get("user_id")
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    user = get_user_with_id(user_id=username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_user_admin(user: User = Depends(get_current_user)):
    if user.role_type!="Admin":
        raise HTTPException(401,"Unauthorized")