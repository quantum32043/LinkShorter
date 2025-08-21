from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user

from backend.auth.auth import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from backend.db import get_db
from backend.models.user import User
from backend.schemas.token import Token
from backend.schemas.user import UserCreateRequest, UserCreateResponse

routes = APIRouter(prefix="/api")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@routes.post('/login', response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or verify_password(user.password_hash, form_data.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token({"sub": user.username})
    refresh_token = create_refresh_token({"sub": user.username})
    return Token(access_token=access_token, refresh_token=refresh_token)


@routes.post('/register', response_model=UserCreateResponse)
def register(user: UserCreateRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exist")

    new_user = User(
        username=user.username,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserCreateResponse(id=new_user.id, username=new_user.username)


@routes.post('/refresh', response_model=Token)
def refresh(refresh_token: str = Body(...), db: Session = Depends(get_db)):
    try:
        payload = decode_token(refresh_token)
        username = payload['sub']
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    new_access_token = create_access_token({"sub": username})
    new_refresh_token = create_refresh_token({"sub": username})

    return Token(access_token=new_access_token, refresh_token=new_refresh_token)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_token(token)
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@routes.get("/me", response_model=UserCreateResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return UserCreateResponse(id=current_user.id, username=current_user.username)
