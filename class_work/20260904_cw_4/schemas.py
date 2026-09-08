# Модели Pydantic (DTO)
from datetime import date
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    TypeAdapter,
    computed_field,
    model_validator,
)

from .utils import calc_bonus_percent, calc_years_worked

class Address(BaseModel):
    city: str
    street: str
    house_number: str


class Employee(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    # id не приходит от клиента — генерируется автоматически при создании объекта.
    # default_factory=uuid4 вызывается КАЖДЫЙ раз заново, поэтому у каждого сотрудника будет свой уникальный id
    # (в отличие от default=..., который вычислился бы один раз при объявлении класса)
    id: UUID = Field(default_factory=uuid4)

    first_name: Annotated[str, Field(min_length=2, max_length=50, description="First name")]
    last_name: Annotated[str, Field(min_length=2, max_length=50, description="Last name")]
    email: EmailStr
    hire_date: date
    salary: Annotated[float, Field(gt=0, description="Base salary, before bonus")]
    address: Address

    # спрашивали на занятии как проверить несколько полей сразу
    @model_validator(mode="after")
    def check_names_are_different(self):
        if self.first_name.lower() == self.last_name.lower():
            raise ValueError("first_name and last_name must not be the same")
        return self

    # вычисляемое поле, в файле (БД) не храним
    @computed_field
    @property
    def years_worked(self) -> int:
        return calc_years_worked(self.hire_date)

    # вычисляемое поле, в файле (БД) не храним
    @computed_field
    @property
    def actual_salary(self) -> float:
        bonus = calc_bonus_percent(self.years_worked)
        return round(self.salary * (1 + bonus), 2)


# Ошибки в Response клиент должен получать в унифицированном виде
class ErrorResponse(BaseModel):
    error: str
    details: list = []


# Для валидации/сериализации списка моделей.
# Список — это не BaseModel и у него нет своих model_validate/model_dump, поэтому нужен TypeAdapter
EmployeeListAdapter = TypeAdapter(list[Employee])