from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Product


async def orm_add_product(session: AsyncSession, data: dict):
    obj = Product(                                                      # Создаем обект нашего товара(класс моделс), беря данные из словаря data из машинного состояния
        name=data["name"],
        description=data["description"],
        price=float(data["price"]),
        image=data["image"]
    )
    session.add(obj)                                                    # Добавляем созданный обьект в сессию БД
    await session.commit()                                              # Сохраняем внессенные изменения в БД