from unittest import result

from flask import sessions
from sqlalchemy import create_engine, select, delete, desc, exists, func
from sqlalchemy.orm import Session, selectinload
from models import User, Address

engine = create_engine('sqlite:///practicum3.db')

with Session(engine) as session:
    # --- Задание 1: Поиск пользователя 'Alice' ---
    stmt = select(User).where(User.name == 'Alice')

    user = session.scalar(stmt)

    if user:
        print(f"Пользователь найден: {user}")
        print(f"ID: {user.id}, Имя: {user.name}, Возраст: {user.age}")
    else:
        print(f"Пользователь с таким именем не найден")

    # --- Задание 2: Пользователи старше 20 лет ---
    stmt = select(User).where(User.age >= 20)
    users = session.scalars(stmt).all()
    print("Users older than 20:")
    print(users)

    target_age = 22
    stmt = select(User).where(User.age == target_age)
    users_with_age = session.scalars(stmt).all()
    print(f"Пользователи, которым ровно {target_age}")
    print(users_with_age)

    print("-" * 40)

    # --- Задание 3: Обновление возраста пользователя "Bob" ---
    stmt_bob = select(User).where(User.name == 'Bob')
    bob = session.scalars(stmt_bob).first()  # .first() корректно возвращает объект User

    if bob:
        print(f"До обновления: {bob.name}, возраст: {bob.age}")

        bob.age = 25
        session.commit()  # Сохраняем изменения в БД

        print(f"Успешно обновлено! Теперь {bob.name}, возраст: {bob.age}")
    else:
        print("Пользователь Bob не найден в базе данных, обновление невозможно.")

    # --- Задание 4: Вывод пользователей моложе 30 лет
    stmt = select(User).where(User.age < 30)
    users = session.scalars(stmt).all()
    print("Users younger than 30:")
    print(users)

    # --- Задание 5: Добавление пользователя
    new_user = User(name='Charlie', age=40)
    session.add(new_user)
    session.commit()

    print("-" * 40)

    # --- Задание 6: Удаление пользователя "Charlie" ---
    # 1. Формируем запрос на удаление
    stmt_delete = delete(User).where(User.name == 'Charlie')

    # 2. Выполняем запрос в сессии
    result = session.execute(stmt_delete)

    # 3. Фиксируем изменения в файле базы данных
    session.commit()

    # 4. Проверяем, сколько строк было затронуто (удалено)
    if result.rowcount > 0:
        print(f"Пользователь 'Charlie' успешно удален из базы данных. (Удалено строк: {result.rowcount})")
    else:
        print("Пользователь 'Charlie' не найден в базе данных. Ничего не удалено.")

    print("-" * 40)

    # --- Задание 7: Вывод пользователей, отсортированных по возрасту (убывание) ---
    # Формируем запрос: SELECT * FROM users ORDER BY age DESC
    stmt_sorted = select(User).order_by(desc(User.age))

    # Получаем весь список пользователей
    sorted_users = session.scalars(stmt_sorted).all()

    print("Список пользователей, отсортированных по возрасту (от старших к младшим):")
    if sorted_users:
        for u in sorted_users:
            print(f"- Имя: {u.name:<10} | Возраст: {u.age}")
    else:
        print("База данных пользователей пуста.")

    print("-" * 40)

    # --- Задание 8: Первые 4 пользователя, отсортированные по имени ---
    # Формируем запрос: SELECT * FROM users ORDER BY name LIMIT 4
    stmt_top4 = select(User).order_by(User.name).limit(4)

    # Получаем результат
    top4_users = session.scalars(stmt_top4).all()

    print("Первые 4 пользователя в алфавитном порядке:")
    if top4_users:
        for u in top4_users:
            print(f"- Имя: {u.name:<10} | Возраст: {u.age} (ID: {u.id})")
    else:
        print("В базе данных нет пользователей.")

    print("-" * 40)

    # --- Задание 9: Обновление возраста пользователя по его id ---
    target_id = 5
    new_age = 35

    # 1. Быстро находим пользователя по его первичному ключу (id)
    user_by_id = session.get(User, target_id)

    if user_by_id:
        print(f"Пользователь с ID {target_id} найден: {user_by_id.name}, старый возраст: {user_by_id.age}")

        # 2. Изменяем возраст
        user_by_id.age = new_age

        # 3. Фиксируем изменения в базе данных
        session.commit()
        print(f"Успешно обновлено! Теперь {user_by_id.name}, новый возраст: {user_by_id.age}")
    else:
        print(f"Пользователь с ID {target_id} не найден в базе данных. Обновление невозможно.")

    print("-" * 40)

    # --- Задание 10: Проверка существования пользователя по имени ---
    search_name = "Charlie"

    # 1. Формируем запрос на проверку существования (генерация SQL-конструкции EXISTS)
    stmt_exists = select(exists().where(User.name == search_name))

    # 2. Выполняем запрос. Метод .scalar() вернет True или False
    user_exists = session.scalar(stmt_exists)

    # 3. Выводим результат проверки
    if user_exists:
        print(f"Пользователь с именем '{search_name}' СУЩЕСТВУЕТ в базе данных.")
    else:
        print(f"Пользователя с именем '{search_name}' НЕТ в базе данных.")

    print("-" * 40)

    # --- Задание 11: Подсчет среднего возраста пользователей ---
    # Формируем запрос: SELECT AVG(age) FROM users
    stmt_avg = select(func.avg(User.age))

    # Выполняем запрос. .scalar() вернет одно число (float) или None, если таблица пуста
    average_age = session.scalar(stmt_avg)

    print("Средний возраст всех пользователей:")
    if average_age is not None:
        # Округляем до одного знака после запятой для красивого вывода
        print(f"Результат: {round(average_age, 1)} лет")
    else:
        print("В базе данных нет пользователей для расчета среднего возраста.")

    print("-" * 40)

    # --- Задание 12: Поиск максимального и минимального возраста ---
    # Формируем запрос: SELECT MAX(age), MIN(age) FROM users
    stmt_extremes = select(func.max(User.age), func.min(User.age))

    # Выполняем запрос и получаем первую строку результата
    result_extremes = session.execute(stmt_extremes).fetchone()

    print("Экстремальные значения возраста среди пользователей:")
    if result_extremes and result_extremes[0] is not None:
        max_age, min_age = result_extremes
        print(f"- Максимальный возраст: {max_age} лет")
        print(f"- Минимальный возраст: {min_age} лет")
    else:
        print("В базе данных нет пользователей для расчета.")

    print("-" * 40)

    # --- Задание 13: Группировка пользователей по возрасту и подсчет их количества ---
    # Формируем запрос: SELECT age, COUNT(id) FROM users GROUP BY age ORDER BY age
    stmt_group = select(User.age, func.count(User.id)).group_by(User.age).order_by(User.age)

    # Выполняем запрос
    grouped_results = session.execute(stmt_group).all()

    print("Количество пользователей по возрастным группам:")
    if grouped_results:
        for age, count in grouped_results:
            print(f"- Возраст: {age} лет -> Количество пользователей: {count}")
    else:
        print("В базе данных нет пользователей для группировки.")

    print("-" * 40)

    # --- Задание 14: Группировка с фильтрацией через HAVING ---
    # Формируем запрос:
    # SELECT age, COUNT(id) FROM users GROUP BY age HAVING COUNT(id) > 1 ORDER BY age
    stmt_having = (
        select(User.age, func.count(User.id))
        .group_by(User.age)
        .having(func.count(User.id) > 1)
        .order_by(User.age)
    )

    # Выполняем запрос
    having_results = session.execute(stmt_having).all()

    print("Возрастные группы, где более одного пользователя:")
    if having_results:
        for age, count in having_results:
            print(f"- Возраст: {age} лет -> Количество пользователей: {count}")
    else:
        print("Нет возрастных групп, в которых количество пользователей больше 1.")

    print("-" * 40)

    # --- Задание 15: Пользователи старше среднего возраста (с исправлением ворнинга) ---
    # ИСПРАВЛЕНИЕ: Вместо .subquery() используем .scalar_subquery()
    subq_avg = select(func.avg(User.age)).scalar_subquery()

    # Теперь SQLAlchemy не будет выдавать предупреждение при сравнении
    stmt_subquery = select(User).where(User.age > subq_avg)

    # Выполняем запрос
    users_above_avg = session.scalars(stmt_subquery).all()

    print("Пользователи старше среднего возраста:")
    if users_above_avg:
        for u in users_above_avg:
            print(f"- Имя: {u.name:<10} | Возраст: {u.age}")
    else:
        print("Нет пользователей старше среднего возраста или база данных пуста.")

    print("-" * 40)

    # --- Задание 16: Вывод всех пользователей вместе с их адресами ---
    # Формируем запрос с жадной загрузкой адресов (JOIN на уровне ORM)
    stmt_with_addresses = select(User).options(selectinload(User.addresses))

    # Выполняем запрос
    users_with_addr = session.scalars(stmt_with_addresses).all()

    print("Список пользователей и их адресов:")
    if users_with_addr:
        for u in users_with_addr:
            print(f"Пользователь: {u.name} (Возраст: {u.age})")

            # Проверяем, есть ли адреса у данного пользователя
            if u.addresses:
                for addr in u.addresses:
                    print(f"  -> Адрес (ID {addr.id}): {addr.description}")
            else:
                print("  -> [Адреса не указаны]")
    else:
        print("В базе данных нет пользователей.")

    print("-" * 40)

    # --- Задание 17: Пользователи, у которых нет адресов ---
    # Формируем запрос: SELECT * FROM users LEFT JOIN addresses ON ... WHERE addresses.id IS NULL
    stmt_no_addresses = (
        select(User)
        .outerjoin(Address)  # Делаем LEFT OUTER JOIN
        .where(Address.id.is_(None))  # Оставляем только тех, у кого нет совпадений по адресу
    )

    # Выполняем запрос
    users_without_addr = session.scalars(stmt_no_addresses).all()

    print("Пользователи без зарегистрированных адресов:")
    if users_without_addr:
        for u in users_without_addr:
            print(f"- Имя: {u.name:<10} | Возраст: {u.age} (ID: {u.id})")
    else:
        print("У всех пользователей есть хотя бы один адрес.")

    print("-" * 40)

    # --- Задание 18: Подсчет количества пользователей в каждом городе ---
    # Формируем запрос: SELECT description, COUNT(user_id) FROM addresses GROUP BY description
    stmt_city_count = (
        select(Address.description, func.count(Address.user_id))
        .group_by(Address.description)
        .order_by(func.count(Address.user_id).desc())
    # Опционально: сортировка от популярных городов к менее популярным
    )

    # Выполняем запрос
    city_results = session.execute(stmt_city_count).all()

    print("Количество пользователей по городам:")
    if city_results:
        for city, count in city_results:
            print(f"- Город: {city:<12} -> Жителей в БД: {count}")
    else:
        print("В таблице адресов нет данных для подсчета.")

    print("-" * 40)
    print("--- Модифицированное Задание 18 (Включая 0 жителей) ---")

    # 1. Строим запрос через select() в стиле SQLAlchemy 2.0
    # Используем func.count(User.id) — он посчитает только существующие ID пользователей,
    # а для пустых связей (NULL) вернет 0.
    stmt = (
        select(Address.description, func.count(User.id))
        .outerjoin(User)  # Делаем LEFT OUTER JOIN, чтобы не терять города без жителей
        .group_by(Address.description)
        .order_by(func.count(User.id).desc())
    )

    # 2. Выполняем запрос
    city_results = session.execute(stmt).all()

    # 3. Выводим ровную таблицу в консоль
    print("Количество пользователей по городам:")
    if city_results:
        for city, count in city_results:
            print(f"- Город: {city:<12} -> Жителей в БД: {count}")
    else:
        print("В таблице адресов нет данных.")

    print("-" * 40)

    # --- Задание 19: Поиск всех пользователей из определенного города ---
    target_city = "Berlin"

    # Формируем запрос: SELECT * FROM users JOIN addresses ON ... WHERE addresses.description = :target_city
    stmt_by_city = (
        select(User)
        .join(Address)  # Объединяем таблицы по настроенной связи
        .where(Address.description == target_city)
    )

    # Выполняем запрос
    users_in_city = session.scalars(stmt_by_city).all()

    print(f"Пользователи, проживающие в городе {target_city}:")
    if users_in_city:
        for u in users_in_city:
            print(f"- Имя: {u.name:<10} | Возраст: {u.age} (ID: {u.id})")
    else:
        print(f"В городе {target_city} никто не зарегистрирован.")

    print("-" * 40)

    # --- Задание 20: Обновление адреса пользователя "Bob" на "Paris" ---
    # 1. Находим пользователя Bob и сразу загружаем его адреса, чтобы избежать N+1
    stmt_bob_addr = select(User).where(User.name == 'Bob').options(selectinload(User.addresses))
    bob_user = session.scalar(stmt_bob_addr)

    if bob_user:
        print(f"Пользователь {bob_user.name} найден.")

        # 2. Проверяем, есть ли у него уже какой-то адрес в таблице
        if bob_user.addresses:
            old_city = bob_user.addresses[0].description
            # Обновляем первый существующий адрес
            bob_user.addresses[0].description = "Paris"
            print(f"Адрес успешно изменен с '{old_city}' на 'Paris'")
        else:
            # Если адреса не было, создаем новый объект адреса и добавляем в список пользователя
            new_address = Address(description="Paris")
            bob_user.addresses.append(new_address)
            print("У пользователя не было адреса. Создан новый адрес: 'Paris'")

        # 3. Фиксируем изменения в базе данных
        session.commit()
    else:
        print("Пользователь Bob не найден в базе данных. Обновление адреса невозможно.")

    # --- Задание 20v2: Обновление адреса пользователя "Bob" на "Rome" ---
    # 1. Находим пользователя Bob и сразу загружаем его адреса, чтобы избежать N+1
    stmt_bob_addr = select(User).where(User.name == 'Bob').options(selectinload(User.addresses))
    bob_user = session.scalar(stmt_bob_addr)

    if bob_user:
        print(f"Пользователь {bob_user.name} найден.")

        # 2. Проверяем, есть ли у него уже какой-то адрес в таблице
        if bob_user.addresses:
            old_city = bob_user.addresses[0].description
            # Обновляем первый существующий адрес
            bob_user.addresses[0].description = "Rome"
            print(f"Адрес успешно изменен с '{old_city}' на 'Rome'")
        else:
            # Если адреса не было, создаем новый объект адреса и добавляем в список пользователя
            new_address = Address(description="Rome")
            bob_user.addresses.append(new_address)
            print("У пользователя не было адреса. Создан новый адрес: 'Rome'")

        # 3. Фиксируем изменения в базе данных
        session.commit()
    else:
        print("Пользователь Bob не найден в базе данных. Обновление адреса невозможно.")