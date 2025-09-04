import string
import random

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth.auth import decode_token
from backend.db import get_db
from backend.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="/api/login", auto_error=False)


def generate_random_string(length: int = 6):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


async def _get_user_from_token(token: str | None, db: AsyncSession) -> User | None:
    if not token:
        return None
    try:
        payload = decode_token(token)
        username = payload.get("sub")
        if username is None:
            return None
        result = await db.execute(select(User).where(User.username == username))
        return result.scalars().first()
    except JWTError:
        return None


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    user = await _get_user_from_token(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user


async def get_optional_user(token: str | None = Depends(oauth2_scheme_optional), db: AsyncSession = Depends(get_db)) -> User | None:
    return await _get_user_from_token(token, db)