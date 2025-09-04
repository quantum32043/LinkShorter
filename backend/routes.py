import os
import uuid
from datetime import datetime

import dotenv
from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from starlette.responses import RedirectResponse
from utils import generate_random_string, get_current_user, get_optional_user

from backend.auth.auth import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from backend.db import get_db
from backend.models.short import Short
from backend.models.user import User
from backend.schemas.short import ShortLinkRequest, ShortLinkResponse
from backend.schemas.token import Token
from backend.schemas.user import UserCreateRequest, UserCreateResponse

routes = APIRouter(prefix="/api")
redirect_route = APIRouter(prefix="")
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


@routes.get("/me", response_model=UserCreateResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return UserCreateResponse(id=current_user.id, username=current_user.username)


@routes.post("/short", response_model=ShortLinkResponse)
async def generate_short_url(
        url: ShortLinkRequest,
        request: Request,
        db: AsyncSession = Depends(get_db),
        user: User | None = Depends(get_optional_user)
):
    exist = True
    short_link = None
    while exist:
        candidate = os.getenv("HOST_NAME") + "short/" + generate_random_string()
        result = await db.execute(select(Short).where(Short.short_link == candidate))
        exist = result.scalars().first()
        if not exist:
            short_link = candidate

    session_id = request.cookies.get("session_id")

    shorted_url = Short(
        session_id=session_id,
        user_id=user.id if user else None,
        original_link=url.original_url,
        short_link=short_link,
        date=datetime.now()
    )

    print(shorted_url)

    response = JSONResponse(
        content=ShortLinkResponse(
            original_url=shorted_url.original_link,
            short_url=shorted_url.short_link,
            date=shorted_url.date
        ).model_dump_json()
    )

    if not user and not session_id:
        session_id = str(uuid.uuid4())
        shorted_url.session_id = session_id
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            secure=True,
            samesite="none",
            max_age=24 * 60 * 60
        )

    db.add(shorted_url)
    await db.commit()
    await db.refresh(shorted_url)

    return response


@redirect_route.get("/short/{short_id}")
async def read_shorts(short_id: str, db: AsyncSession = Depends(get_db)):
    unique_url = os.getenv("HOST_NAME") + "short/" + short_id
    print("HOST_NAME:", os.getenv("HOST_NAME"))
    print("short_id:", short_id)
    print("unique_url:", unique_url)

    result = await db.execute(select(Short).where(Short.short_link == unique_url))
    short = result.scalars().first()
    print("short from DB:", short)

    return RedirectResponse(url=short.original_link)


@routes.get("/history")
async def read_history(db: AsyncSession = Depends(get_db)):
    pass
