from datetime import date, timedelta
from pydantic import ValidationError
from models import User


def register_user(json_str: str) -> str:
    try:
        user = User.model_validate_json(json_str)
        return f"УСПЕХ! Зарегистрирован: {user.name}, Возраст: {user.age}"
    except ValidationError as e:
        return f"ОШИБКА ВАЛИДАЦИИ:\n{e}"


# Динамически вычисляем даты для теста (чтобы тесты работали корректно в любой день)
today = date.today()
date_exactly_18 = (today - timedelta(days=18 * 365.25)).isoformat()  # Ровно 18 лет назад
date_almost_18 = (
    today - timedelta(days=18 * 365.25) + timedelta(days=1)
).isoformat()  # 18 лет без одного дня (еще 17)

# --- ТЕСТОВЫЕ СЦЕНАРИИ ---

# 1. Успех: Пользователю сегодня исполнилось ровно 18 лет, и он работает
json_exactly_18 = f"""{{
    "name": "Adult Ivan",
    "birth_date": "{date_exactly_18}",
    "email": "ivan@example.com",
    "is_employed": true,
    "address": {{
        "city": "Moscow",
        "street": "Arbat",
        "house_number": 12
    }}
}}"""

# 2. Ошибка: Пользователю исполнится 18 только завтра. Сегодня ему 17, и он работает (Запрещено!)
json_almost_18_employed = f"""{{
    "name": "Young Teen",
    "birth_date": "{date_almost_18}",
    "email": "teen@example.com",
    "is_employed": true,
    "address": {{
        "city": "Moscow",
        "street": "Arbat",
        "house_number": 12
    }}
}}"""

# 3. Успех: Пользователю 17 лет, но он НЕ работает (Разрешено по логике модели)
json_almost_18_unemployed = f"""{{
    "name": "Free Teen",
    "birth_date": "{date_almost_18}",
    "email": "teen2@example.com",
    "is_employed": false,
    "address": {{
        "city": "Moscow",
        "street": "Arbat",
        "house_number": 12
    }}
}}"""

if __name__ == "__main__":
    print("--- Тест: Ровно 18 лет + Работает ---")
    print(register_user(json_exactly_18))

    print("\n--- Тест: Еще 17 лет + Работает (Ожидаем ошибку) ---")
    print(register_user(json_almost_18_employed))

    print("\n--- Тест: Еще 17 лет + НЕ работает ---")
    print(register_user(json_almost_18_unemployed))
