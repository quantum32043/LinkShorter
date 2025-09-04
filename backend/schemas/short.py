import uuid
from datetime import datetime

from pydantic import BaseModel


class ShortLinkBase(BaseModel):
    original_url: str


class ShortLinkResponse(ShortLinkBase):
    short_url: str
    date: datetime


class ShortLinkRequest(ShortLinkBase):
    pass
