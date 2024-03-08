from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from database.models import Product



# Функция добавления товара
async def orm_add_product(session: AsyncSession, data: dict):
    obj = Product(                                                      # Создаем обект нашего товара(класс моделс), беря данные из словаря data из машинного состояния
        name=data["name"],
        description=data["description"],
        price=float(data["price"]),
        image=data["image"])
    session.add(obj)                                                    # Добавляем созданный обьект в сессию БД
    await session.commit()                                              # Сохраняем внессенные изменения в БД



# Функция для получения всех товаров
async def orm_get_all_products(session: AsyncSession):
    query = select(Product)
    result = await session.execute(query)
    return result.scalars().all()



# Функция для получения одного товара
async def orm_get_product(session: AsyncSession, product_id: int):
    query = select(Product).where(Product.id == product_id)
    result = await session.execute(query)
    return result.scalar()



# Функция для обновления товара
async def orm_update_product(session: AsyncSession, product_id: int, data: dict):
    query = update(Product).where(Product.id == product_id).values(
        name=data["name"],
        description=data["description"],
        price=float(data["price"]),
        image=data["image"],)
    await session.execute(query)
    await session.commit()


# Функция для удаления товара
async def orm_delete_product(session: AsyncSession, product_id: int):
    query = delete(Product).where(Product.id == product_id)
    await session.execute(query)
    await session.commit()