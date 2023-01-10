from database_classes import Table, UsersTable, PurchasesTable, ProductsTable
from config import BASIC_LANGUAGE


class MainClassBase:
    def __init__(self, table):
        self.__table: Table = table
        self.__tb_id = None


class User(MainClassBase):
    def __init__(self, table: UsersTable, user_id: int):
        super().__init__(table)

        self.user_id: int = int(user_id)
        self.language = BASIC_LANGUAGE
        self.purchases: [Purchase] = []
        self.baned: bool = False

    async def find_language(self):
        pass

    async def __set_tb_id(self):
        self.__tb_id = await self.__table.select_vals(user_id=self.user_id)["id"]
        return self.__tb_id

    async def insert_user(self):
        return await self.__table.insert_vals(user_id=int(user_id))


class Purchase(MainClassBase):
    def __init__(self, table: PurchasesTable, user: User = None, date: str = "", product: Product = None):
        super().__init__(table)

        self.user: User = user
        self.date = date
        self.product: Product = product


class Product(MainClassBase):
    def __init__(self, table: ProductsTable):
        super().__init__(table)

        self.title: str = None
        self.price: int = None
        self.description: str = None
        self.vid_amount: int = None
