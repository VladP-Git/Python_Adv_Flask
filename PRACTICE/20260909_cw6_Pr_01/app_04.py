from pydantic import BaseModel, field_validator
from datetime import datetime, timedelta

class Appointment(BaseModel):
    patient_name: str
    appointment_date: datetime

    # Используем современный декоратор вместо @validator
    @field_validator('appointment_date')
    def check_appointment_date(cls, v: datetime) -> datetime:
        if v < datetime.now() + timedelta(days=1):
            raise ValueError("Appointment must be scheduled at least 24 hours in advance.")
        return v

# Пример использования
try:
    appointment = Appointment(patient_name="Alice Smith", appointment_date=datetime.now() + timedelta(hours=25))
    print(appointment)
except ValueError as e:
    print(e)