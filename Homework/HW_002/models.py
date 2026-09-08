from datetime import date
from pydantic import BaseModel, EmailStr, Field, model_validator


class Address(BaseModel):
    city: str = Field(..., min_length=2)
    street: str = Field(..., min_length=3)
    house_number: int = Field(..., gt=0)


class User(BaseModel):
    # name: минимум 2 символа, регулярное выражение разрешает только буквы и пробелы
    name: str = Field(..., min_length=2, pattern=r"^[a-zA-Zа-яА-Я\s]+$")
    birth_date: date  # Принимает строку "YYYY-MM-DD"
    age: int = Field(default=0, ge=0, le=120)  # Будет вычисляться автоматически
    email: EmailStr
    is_employed: bool
    address: Address

    # Кастомный валидатор для проверки соответствия возраста и занятости
    # 1. Вычисляем возраст ДО основной валидации полей
    @model_validator(mode='before')
    @classmethod
    def calculate_age(cls, data: dict) -> dict:
        # Проверяем, что данные пришли в виде словаря и есть дата рождения
        if isinstance(data, dict) and 'birth_date' in data:
            try:
                # Если дата пришла строкой, превращаем её в объект date для расчета
                b_date = date.fromisoformat(data['birth_date'])
                today = date.today()

                # Формула точного расчета возраста с учетом месяцев и дней
                computed_age = today.year - b_date.year - ((today.month, today.day) < (b_date.month, b_date.day))

                # Записываем вычисленный возраст в данные
                data['age'] = computed_age
            except (ValueError, TypeError):
                # Если формат даты совсем сломан, пропускаем — Pydantic сам выдаст ошибку на поле birth_date
                pass
        return data

    # 2. Проверяем соответствие возраста и занятости ПОСЛЕ сборки модели
    @model_validator(mode='after')
    def check_employment_age(self) -> 'User':
        if self.is_employed and not (18 <= self.age <= 65):
            raise ValueError(
                f"Занятой пользователь (is_employed=True) должен быть в возрасте от 18 до 65 лет. "
                f"Вычисленный возраст: {self.age} (Дата рождения: {self.birth_date})."
            )
        return self
