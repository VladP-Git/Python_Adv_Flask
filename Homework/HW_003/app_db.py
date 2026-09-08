import logging
from decimal import Decimal
from sqlalchemy import create_engine, ForeignKey, String, Numeric, Boolean
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('sqlalchemy.engine')
logger.setLevel(logging.DEBUG)

# Базовый класс для моделей
class Base(DeclarativeBase):
    pass


# --- ЗАДАЧА 4: Модель Категории ---
class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))


# --- ЗАДАЧА 3 & 5: Модель Продукта ---
class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True)

    # ЗАДАЧА 5: Устанавливаем связь через ForeignKey.
    # Указываем строку 'имя_таблицы.колонка' -> 'categories.id'
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id', ondelete='CASCADE'))


# --- ЗАДАЧА 1: Движок для SQLite ---
engine = create_engine('sqlite:///cafe.sqlite3')

# --- ЗАДАЧА 2: Сессия для взаимодействия ---
Session = sessionmaker(bind=engine)

# --- ТЕСТОВЫЙ ЗАПУСК ДЛЯ ПРОВЕРКИ ---
if __name__ == "__main__":
    # Создаем таблицы в базе данных
    Base.metadata.create_all(engine)
    print("\n[ СХЕМА БАЗЫ ДАННЫХ УСПЕШНО СОЗДАНА ]\n")

    # Проверяем работу сессии и связей
    with Session() as session:
        # 1. Создаем и добавляем категорию
        food_category = Category(name="Еда", description="Выпечка и десерты")
        session.add(food_category)

        # flush() отправляет данные в БД, чтобы SQLite сгенерировал id для категории
        session.flush()

        # 2. Создаем продукт и связываем его через числовой id категории
        croissant = Product(
            name="Круассан",
            price=Decimal("180.00"),
            in_stock=True,
            category_id=food_category.id  # Передаем полученный id
        )
        session.add(croissant)

        # Сохраняем всё в базу
        session.commit()
        print("\n[ ДАННЫЕ УСПЕШНО СОХРАНЕНЫ ]")
