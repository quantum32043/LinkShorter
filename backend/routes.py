import os

import dotenv
from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user

from backend.auth.auth import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from backend.db import get_db
from backend.models.user import User
from backend.schemas.token import Token
from backend.schemas.user import UserCreateRequest, UserCreateResponse

routes = APIRouter(prefix="/api")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")
dotenv.load_dotenv()


@routes.post('/login', response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalars().first()
    if not user or not verify_password(user.password_hash, form_data.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token({"sub": user.username})
    refresh_token = create_refresh_token({"sub": user.username})
    await db.execute(update(User).where(User.username == user.username).values(refresh_token=refresh_token))
    await db.commit()
    response = JSONResponse(status_code=200, content={"access_token": access_token})
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")) * 24 * 60 * 60
    )
    return response


@routes.post('/register', response_model=UserCreateResponse)
async def register(user: UserCreateRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == user.username))
    existing = result.scalars().first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exist")

    new_user = User(
        username=user.username,
        password_hash=hash_password(user.password)
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return UserCreateResponse(id=new_user.id, username=new_user.username)


@routes.post('/refresh', response_model=Token)
async def refresh(request: Request, db: AsyncSession = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=403, detail="No refresh token")
    try:
        payload = decode_token(refresh_token)
        username = payload['sub']
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid or expired token")

    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user or user.refresh_token != refresh_token:
        raise HTTPException(status_code=403, detail="Invalid refresh token")

    new_access_token = create_access_token({"sub": username})
    new_refresh_token = create_refresh_token({"sub": username})

    await db.execute(update(User).where(User.username == username).values(refresh_token=new_refresh_token))
    await db.commit()

    response = JSONResponse(status_code=200, content={"access_token": new_access_token})
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")) * 24 * 60 * 60
    )

    return response


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        payload = decode_token(token)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@routes.get("/me", response_model=UserCreateResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return UserCreateResponse(id=current_user.id, username=current_user.username)


# @routes.post("/short", response_model=)
