from typing import Annotated, List
from pydantic import BaseModel, EmailStr, ValidationError, Field, HttpUrl, field_validator, ConfigDict


# Переиспользуемый "типизированный фрагмент" через Annotated:
# любое поле с типом positive_number будет float и обязано быть > 0 (gt=0).
# Удобно, когда одно и то же правило валидации нужно в нескольких моделях —
# не приходится дублировать Field(gt=0) в каждой модели отдельно.
positive_number = Annotated[float, Field(gt=0)]


class Product(BaseModel):
    name: str
    description: Annotated[str | None, Field(default=None, description='Description of product')]

    # Используем заранее описанный тип positive_number — цена всегда > 0
    price: positive_number
    in_stock: Annotated[bool, Field(description='Whether product is in stock')] = False
    tags: list[str]
    url: HttpUrl


class Order(BaseModel):
    total: positive_number


class Address(BaseModel):
    house_number: str
    street: str
    city: str


class User(BaseModel):
    # Конфигурация модели через актуальный (не deprecated) способ —
    # ConfigDict вместо старого внутреннего класса Config
    model_config = ConfigDict(
        str_strip_whitespace=True,   # обрезает пробелы по краям строк ("  John  " -> "John")
        str_to_upper=True,           # переводит ВСЕ строковые поля модели в верхний регистр
        str_min_length=3             # минимальная длина для всех строковых полей — 3 символа
    )

    id: int

    # min_length/max_length работают на уровне ОТДЕЛЬНОГО поля и здесь
    # дублируют/уточняют общий str_min_length=3 из model_config
    name: Annotated[str, Field(min_length=3, max_length=50, description='Name of user')]
    age: Annotated[int, Field(ge=18, le=70, description='Age of user')]
    email: Annotated[EmailStr, Field(description='Email of user')]
    is_active: bool = True
    address: Address

    # --- Старый (deprecated) способ конфигурации оставлен закомментированным
    # --- для сравнения с актуальным model_config выше. В реальном коде
    # --- использовать не нужно.
    # class Config:
    #     str_strip_whitespace = True
    #     str_min_length = 3

    # @field_validator('name')
    # def check_name(cls, value):
    #     if value.istitle():
    #         return value
    #     raise ValueError('Name must be in title notation')

    # Кастомный валидатор для email: разрешены только домены gmail.com и yahoo.com.
    # Декоратор @field_validator('email') говорит Pydantic вызвать этот метод
    # ПОСЛЕ того, как значение прошло базовую проверку типа EmailStr.
    @field_validator('email')
    def check_email(cls, value):
        allowed_domains = ['gmail.com', 'yahoo.com']

        _, domain = value.split('@')          # разделяем строку по @ на логин и домен
        if domain not in allowed_domains:
            raise ValueError('Invalid email address')  # именно ValueError, не ValidationError
        return value                            # обязательно вернуть значение обратно

    # Обычный метод модели — не имеет отношения к валидации,
    # просто пользовательская бизнес-логика
    def greetings(self):
        return f'Hello, {self.name}'

    # Переопределяем __str__, чтобы print(user) выводил только имя,
    # а не полное представление модели по умолчанию
    def __str__(self):
        return f'{self.name}'


# Наследование: Admin получает ВСЕ поля и методы User + добавляет своё поле
class Admin(User):
    is_admin: bool = True


# --- Создание объектов "вручную", через именованные аргументы ---
addr_1 = Address(city='NY', street='San Francisco', house_number='10')
user_1 = User(id=1, name='     John    ', age=20, is_active=True, address=addr_1, email='example@gmail.com')
print(user_1)


# --- Создание объекта из "внешних" данных, например пришедших по API ---

json_string = """{
    "id": 1,
    "name": "John Doe",
    "age": 22.0,
    "email": "john.doe@example.com",
    "is_active": 0,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": "123"
    }
}"""

try:
    user = User.model_validate_json(json_string, strict=False)
    print(user)
    user.age += 10
    res = user.model_dump_json(indent=4)
    print(res)
except ValidationError as e:
    print(f'ValidationError: {e}')