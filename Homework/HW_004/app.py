import logging
from decimal import Decimal
from sqlalchemy import create_engine, ForeignKey, String, Numeric, Boolean, select, func
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column, relationship

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('sqlalchemy.engine')


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255))

    # Связь один-ко-многим с подгрузкой selectin
    products: Mapped[list['Product']] = relationship(back_populates='category', lazy='selectin')

    def __repr__(self) -> str:
        return f"Категория: {self.name}"


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True)

    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id', ondelete='CASCADE'))
    category: Mapped['Category'] = relationship(back_populates='products')

    def __repr__(self) -> str:
        return f"Продукт: {self.name} (Цена: {self.price})"


# Файл базы данных
engine = create_engine('sqlite:///shop2.sqlite', echo=False)
Base.metadata.drop_all(engine)  # Сбрасываем старые таблицы для чистоты тестов
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# ==========================================
# ЗАДАЧА 1: Наполнение данными
# ==========================================
with Session() as session:
    # Создаем категории
    el = Category(name="Электроника", description="Гаджеты и устройства.")
    books = Category(name="Книги", description="Печатные книги и электронные книги.")
    clothes = Category(name="Одежда", description="Одежда для мужчин и женщин.")
    sport = Category(name="Спорттовары", description="Товары для спорта.")

    session.add_all([el, books, clothes, sport])
    session.flush()  # Получаем ID категорий из базы данных

    # Создаем продукты и привязываем их через category_id
    p1 = Product(name="Смартфон", price=Decimal("299.99"), in_stock=True, category_id=el.id)
    p2 = Product(name="Ноутбук", price=Decimal("499.99"), in_stock=True, category_id=el.id)
    p3 = Product(name="Научно-фантастический роман", price=Decimal("15.99"), in_stock=True, category_id=books.id)
    p4 = Product(name="Джинсы", price=Decimal("40.50"), in_stock=True, category_id=clothes.id)
    p5 = Product(name="Футболка", price=Decimal("20.00"), in_stock=True, category_id=clothes.id)

    session.add_all([p1, p2, p3, p4, p5])
    session.commit()
    print("[ Задача 1 ]: Данные успешно добавлены!\n")

# ==========================================
# ЗАДАЧА 2: Чтение данных (Категории + Продукты)
# ==========================================
print("-" * 50)
print("[ Задача 2 ]: Список категорий и их продуктов:")
with Session() as session:
    # Запрашиваем все категории
    categories = session.scalars(select(Category)).all()
    for cat in categories:
        print(f"\n{cat.name} ({cat.description}):")
        # Благодаря relationship и lazy='selectin' продукты доступны сразу без JOIN-ов
        for prod in cat.products:
            print(f"  - {prod.name}: {prod.price} руб.")
print("-" * 50)

# ==========================================
# ЗАДАЧА 3: Обновление данных
# ==========================================
with Session() as session:
    # Ищем первый Смартфон
    smartphone = session.scalars(select(Product).where(Product.name == "Смартфон")).first()
    if smartphone:
        smartphone.price = Decimal("349.99")  # Меняем цену
        session.commit()
        print(f"[ Задача 3 ]: Цена на '{smartphone.name}' успешно обновлена до {smartphone.price}\n")

# ==========================================
# ЗАДАЧА 4: Агрегация и группировка
# ==========================================
print("-" * 50)
print("[ Задача 4 ]: Количество продуктов в каждой категории:")
with Session() as session:
    # Соединяем продукт с категорией, группируем по имени категории и считаем количество ID продуктов
    # Используем .outerjoin() вместо .join()
    query = (
        select(Category.name, func.count(Product.id).label('total_products'))
        .outerjoin(Product) # Гарантирует, что пустые категории тоже попадут в отчет
        .group_by(Category.name)
    )
    for row in session.execute(query):
        print(f"Категория '{row.name}' -> Всего продуктов: {row.total_products}")
print("-" * 50)

# ==========================================
# ЗАДАЧА 5: Группировка с фильтрацией (HAVING)
# ==========================================
print("[ Задача 5 ]: Категории, в которых более одного продукта:")
with Session() as session:
    # Используем .having() чтобы отсечь группы, где товаров <= 1
    query = (
        select(Category.name, func.count(Product.id).label('total_products'))
        .join(Product)
        .group_by(Category.name)
        .having(func.count(Product.id) > 1)
    )
    for row in session.execute(query):
        print(f"Категория '{row.name}' (Количество: {row.total_products})")
print("-" * 50)