from pydantic import BaseModel, field_validator
from datetime import datetime, timedelta


class Event(BaseModel):
    title: str
    date: datetime
    location: str

    @field_validator('date')
    @classmethod
    def date_must_be_future(cls, v):
        if v < datetime.now():
            raise ValueError("Event date must be in the future")
        return v

# Пример использования
try:
    future_event = Event(title="New Year Party", date=datetime.now() + timedelta(days=30),
location="New York")
    print(future_event)
except ValueError as e:
    print(e)


