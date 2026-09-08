import json
from datetime import date
from .settings import DATA_FILE


def calc_years_worked(hire_date: date) -> int:
    today = date.today()
    years = today.year - hire_date.year - ((today.month, today.day) < (hire_date.month, hire_date.day))
    return years


# Логика: стаж и надбавка за стаж
# 0-3 года -> +0%, 3-5 -> +10%, 5-10 -> +20%, 10+ -> +30%
def calc_bonus_percent(years: int) -> float:
    if years < 3:
        return 0.0
    if years < 5:
        return 0.10
    if years < 10:
        return 0.20
    return 0.30


def load_employees() -> list:
    from .schemas import Employee
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            raw_list = json.load(f)
    except FileNotFoundError:
        return []
    return [Employee(**item) for item in raw_list]


def save_employees(employees: list) -> None:
    # years_worked/actual_salary исключаем из файла — это вычисляемые поля и их не нужно сохранять
    data = [
        e.model_dump(mode="json", exclude={"years_worked", "actual_salary"})
        for e in employees
    ]
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
