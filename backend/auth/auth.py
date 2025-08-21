import os
from datetime import datetime, timedelta

import dotenv
from jose import jwt, JWTError
from passlib.context import CryptContext

context = CryptContext(schemes=["bcrypt"], deprecated="auto")
dotenv.load_dotenv()


def hash_password(password: str) -> str:
    return context.hash(password)


def verify_password(hashed_password: str, password: str) -> bool:
    return context.verify(password, hashed_password)


def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, algorithm=os.getenv("ALGORITHM"), key=os.getenv("SECRET_KEY"))


def create_access_token(data: dict):
    return create_token(data=data, expires_delta=timedelta(minutes=float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))))


def create_refresh_token(data: dict):
    return create_token(data=data, expires_delta=timedelta(days=float(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))))


def decode_token(token: str):
    try:
        payload = jwt.decode(token, key=os.getenv("SECRET_KEY"), algorithms=os.getenv("ALGORITHM"))
        return payload
    except JWTError:
        return None
