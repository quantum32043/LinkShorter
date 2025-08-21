from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreateRequest(UserBase):
    password: str


class UserCreateResponse(UserBase):
    id: int
