from datetime import datetime

from pydantic import BaseModel


class Event(BaseModel):
    summary: str
    start_datetime: datetime
    end_datetime: datetime
