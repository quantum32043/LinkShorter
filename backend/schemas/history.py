from datetime import datetime


class HistoryBase:
    pass


class HistoryCreateResponse:
    user_id: int
    original_link: str
    short_link: str
    date: datetime

# class HistoryCreateRequest():
