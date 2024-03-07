from database.engine import drop_db, create_db


async def on_startup(bot):
    run_param = False                                   # Как для примера, переменная от которой можно удалить БД и создать заново

    if run_param:
        await drop_db()

    await create_db()



async def on_shutdown(bot):
    print("Бот остановлен!")