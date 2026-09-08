from pydantic import ValidationError
from models import User


def register_user(json_str: str) -> str:
    try:
        user = User.model_validate_json(json_str)
        return user.model_dump_json(indent=4)
    except ValidationError as e:
        return f"Ошибка валидации:\n{e}"


# --- ТЕСТОВЫЕ СЦЕНАРИИ ---

# 1. Успех: Работающий взрослый (родился в 2000 году, сейчас ему ~26 лет)
json_success_working = """{
    "name": "Ivan Ivanov",
    "birth_date": "2000-05-15",
    "email": "ivan@example.com",
    "is_employed": true,
    "address": {
        "city": "Moscow",
        "street": "Arbat",
        "house_number": 12
    }
}"""

# 2. Ошибка: Работает, но по дате рождения ему уже 76 лет (родился в 1950)
json_error_too_old = """{
    "name": "John Doe",
    "birth_date": "1950-03-10",
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}"""

# 3. Ошибка: Некорректный формат даты
json_error_invalid_date = """{
    "name": "Anna",
    "birth_date": "15-05-2000",
    "email": "anna@example.com",
    "is_employed": false,
    "address": {
        "city": "Berlin",
        "street": "Hauptstrasse",
        "house_number": 4
    }
}"""

if __name__ == "__main__":
    print("--- Тест 1: Успех (Авто-вычисление возраста для работающего) ---")
    print(register_user(json_success_working))

    print("\n--- Тест 2: Ошибка валидатора занятости (Слишком старый по дате рождения) ---")
    print(register_user(json_error_too_old))

    print("\n--- Тест 3: Ошибка неверного формата даты ---")
    print(register_user(json_error_invalid_date))
