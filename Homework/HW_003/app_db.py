import logging
from decimal import Decimal
from sqlalchemy import create_engine, ForeignKey, String, Numeric, Boolean
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('sqlalchemy.engine')
logger.setLevel(logging.DEBUG)


# Базовый класс для моделей
class Base(DeclarativeBase):
    pass


# --- ЗАДАЧА 4 & 5: Модель Категории ---
class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))

    # Связь relationship - более удобный доступ к продуктам категории из Python
    products: Mapped[list["Product"]] = relationship("Product", back_populates="category")


# --- ЗАДАЧА 3 & 5: Модель Продукта ---
class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Numeric(10, 2) — число с фиксированной точностью (например, 1025.50)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    # Boolean — логическое значение (True/False)
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True)

    # ЗАДАЧА 5: Внешний ключ (ForeignKey) связывает продукт с id категории
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id', ondelete='CASCADE'))

    # Связь (relationship) для доступа к объекту категории из объекта продукта
    category: Mapped["Category"] = relationship("Category", back_populates="products")


# --- ЗАДАЧА 1: Движок для SQLite в памяти (in-memory) ---
# Название ':memory:' означает, что база создается в оперативной памяти и исчезнет после закрытия программы
engine = create_engine('sqlite:///:memory:', echo=True)

# --- ЗАДАЧА 2: Создание фабрики сессий ---
Session = sessionmaker(bind=engine)

# --- ТЕСТОВЫЙ ЗАПУСК ДЛЯ ПРОВЕРКИ ---
if __name__ == "__main__":
    # Создаем таблицы в нашей базе данных в памяти
    Base.metadata.create_all(engine)
    print("\n[ СХЕМА БАЗЫ ДАННЫХ УСПЕШНО СОЗДАНА ]\n")

    # Открываем сессию для работы с данными
    with Session() as session:
        # 1. Создаем категорию
        coffee_category = Category(name="Кофе", description="Зерновой и молотый кофе")
        session.add(coffee_category)
        session.flush()  # flush() отправляет запрос в БД, чтобы у категории появился id

        # 2. Создаем продукт, привязанный к этой категории через id
        cappuccino = Product(
            name="Капучино Бленд",
            price=Decimal("450.00"),
            in_stock=True,
            category_id=coffee_category.id
        )
        session.add(cappuccino)
        session.commit()

        print("\n[ ДАННЫЕ УСПЕШНО ДОБАВЛЕНЫ И СВЯЗАНЫ ]")