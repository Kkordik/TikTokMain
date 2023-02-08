import asyncio
from database.database_classes import Database, UsersTable, VideosTable, ProductsTable, PurchasesTable, TextsTable
from config import HOST, USER, PASSWORD, NAME, PORT


async def run_db(_loop, host, user, password, name, port):
    db = Database(host, user, password, name, port)
    await db.make_pool(_loop)
    return db


if __name__ == "database.run_main_db":
    # Register database and pool
    loop = asyncio.get_event_loop()
    main_db = loop.run_until_complete(run_db(loop, HOST, USER, PASSWORD, NAME, PORT))

    # Register main tables
    user_tb = UsersTable(main_db)
    video_tb = VideosTable(main_db)
    prod_tb = ProductsTable(main_db)
    purch_tb = PurchasesTable(main_db)
    text_tb = TextsTable(main_db)
