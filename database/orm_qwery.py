import math

from aiogram.types import Message
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database.models import Banner, Cart, Category, Product, User, Sold


#______________________________________________________Paginator_________________________________________________
class Paginator:
    def __init__(self, array: list | tuple, page: int=1, per_page: int=1):
        self.array = array
        self.per_page = per_page
        self.page = page
        self.len = len(self.array)
        # math.ceil - округление в большую сторону до целого числа
        self.pages = math.ceil(self.len / self.per_page)

    def __get_slice(self):
        start = (self.page - 1) * self.per_page
        stop = start + self.per_page
        return self.array[start:stop]

    def get_page(self):
        page_items = self.__get_slice()
        return page_items

    def has_next(self):
        if self.page < self.pages:
            return self.page + 1
        return False

    def has_previous(self):
        if self.page > 1:
            return self.page - 1
        return False

    def get_next(self):
        if self.page < self.pages:
            self.page += 1
            return self.get_page()
        raise IndexError(f'Next page does not exist. Use has_next() to check before.')

    def get_previous(self):
        if self.page > 1:
            self.page -= 1
            return self.__get_slice()
        raise IndexError(f'Previous page does not exist. Use has_previous() to check before.')



#____________________________________ Админка: добавить/изменить/удалить товар ________________________________

# Функция добавления товара
async def orm_add_product(session: AsyncSession, data: dict):
    obj = Product(                                                      # Создаем обект нашего товара(класс моделс), беря данные из словаря data из машинного состояния
        name=data["name"],
        description=data["description"],
        category_id=int(data["category"]),
        price=float(data["price"]),
        image=data["image"])
    session.add(obj)                                                    # Добавляем созданный обьект в сессию БД
    await session.commit()                                              # Сохраняем внессенные изменения в БД



# Функция для получения всех товаров
async def orm_get_all_products(session: AsyncSession, category_id):
    query = select(Product).where(Product.category_id == int(category_id))
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
        category_id=int(data["category"]),
        price=float(data["price"]),
        image=data["image"],)
    await session.execute(query)
    await session.commit()


# Функция для удаления товара
async def orm_delete_product(session: AsyncSession, product_id: int):
    query = delete(Product).where(Product.id == product_id)
    await session.execute(query)
    await session.commit()




#___________________________________________ Работа с баннерами (информационными страницами)___________________________________


async def orm_add_banner_description(session: AsyncSession, data: dict):
    #Добавляем новый или изменяем существующий по именам
    #пунктов меню: main, about, cart, shipping, payment, catalog
    query = select(Banner)
    result = await session.execute(query)
    if result.first():
        return
    session.add_all([Banner(name=name, description=description) for name, description in data.items()])
    await session.commit()


async def orm_change_banner_image(session: AsyncSession, name: str, image: str):
    query = update(Banner).where(Banner.name == name).values(image=image)
    await session.execute(query)
    await session.commit()


async def orm_get_banner(session: AsyncSession, page: str):
    query = select(Banner).where(Banner.name == page)
    result = await session.execute(query)
    return result.scalar()


async def orm_get_info_pages(session: AsyncSession):
    query = select(Banner)
    result = await session.execute(query)
    return result.scalars().all()


#______________________________________________________ Категории ___________________________________________________

async def orm_get_categories(session: AsyncSession):
    query = select(Category)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_create_categories(session: AsyncSession, categories: list):
    query = select(Category)
    result = await session.execute(query)
    if result.first():
        return
    session.add_all([Category(name=name) for name in categories])
    await session.commit()


#___________________________________________________ Добавляем юзера в БД _________________________________________

async def orm_add_user(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
    phone: str | None = None,
):
    query = select(User).where(User.user_id == user_id)
    result = await session.execute(query)
    if result.first() is None:
        session.add(
            User(user_id=user_id, first_name=first_name, last_name=last_name, phone=phone)
        )
        await session.commit()


#________________________________________________ Работа с корзинами ___________________________________________

async def orm_add_to_cart(session: AsyncSession, user_id: int, product_id: int):
    query = select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id).options(joinedload(Cart.product))
    cart = await session.execute(query)
    cart = cart.scalar()
    if cart:
        cart.quantity += 1
        await session.commit()
        return cart
    else:
        session.add(Cart(user_id=user_id, product_id=product_id, quantity=1))
        await session.commit()



async def orm_get_user_carts(session: AsyncSession, user_id):
    query = select(Cart).filter(Cart.user_id == user_id).options(joinedload(Cart.product))
    result = await session.execute(query)
    return result.scalars().all()


async def orm_delete_from_cart(session: AsyncSession, user_id: int, product_id: int):
    query = delete(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id)
    await session.execute(query)
    await session.commit()


async def orm_reduce_product_in_cart(session: AsyncSession, user_id: int, product_id: int):
    query = select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id).options(joinedload(Cart.product))
    cart = await session.execute(query)
    cart = cart.scalar()

    if not cart:
        return
    if cart.quantity > 1:
        cart.quantity -= 1
        await session.commit()
        return True
    else:
        await orm_delete_from_cart(session, user_id, product_id)
        await session.commit()
        return False



#________________________________________Для работы с совершенными покупками________________________


async def orm_add_to_sold(session: AsyncSession, message: Message, product_id: int):
    query = select(Sold).where(Sold.user_id == message.from_user.id, Sold.product_id == product_id)
    sold_entry = await session.execute(query)
    sold_entry = sold_entry.scalar()

    if sold_entry is not None:
        sold_entry.quantity += 1
        sold_entry.total_sum = sold_entry.quantity * sold_entry.product.price
    else:
        query = select(Cart).where(Cart.user_id == message.from_user.id, Cart.product_id == product_id)
        cart = await session.execute(query)
        cart = cart.scalar()

        if cart is not None:
            product = cart.product
            product_name = product.name
            user_id = message.from_user.id
            name = message.from_user.first_name
            address = message.successful_payment.order_info.shipping_address.street_line1
            phone = message.successful_payment.order_info.phone_number
            quantity = cart.quantity
            total_sum = product.price * quantity

            sold_entry = Sold(
                user_id=user_id,
                user_name = name,
                address = address,
                phone = phone,
                product_id=product_id,
                product_name=product_name,
                quantity=quantity,
                total_sum=total_sum
            )
            session.add(sold_entry)
    await session.commit()



async def orm_delete_cart_after_pay(session: AsyncSession, user_id: int):
    query = delete(Cart).where(Cart.user_id == user_id)
    await session.execute(query)
    await session.commit()




