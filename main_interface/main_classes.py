from database.database_classes import Table, UsersTable, PurchasesTable, ProductsTable
from config import BASIC_LANGUAGE


class MainClassBase:
    def __init__(self, table):
        self.table = table
        self.tb_id = None


class User(MainClassBase):
    def __init__(self, table: UsersTable, user_id: int):
        super().__init__(table)

        self.user_id: int = int(user_id)
        self.language = BASIC_LANGUAGE
        self.purchases: [Purchase] = []
        self.baned: bool = False

    async def __get_tb_id(self):
        self.tb_id = await self.table.select_vals(user_id=self.user_id)["id"]
        return self.tb_id

    async def insert_user(self, user_id=None):
        if user_id:
            self.user_id = int(user_id)
        return await self.table.insert_vals(user_id=int(self.user_id))


class Product(MainClassBase):
    def __init__(self, table: ProductsTable):
        super().__init__(table)

        self.title: str = None
        self.price: int = None
        self.description: str = None
        self.vid_amount: int = None


class Purchase(MainClassBase):
    def __init__(self, table: PurchasesTable, user: User = None, date: str = "", product: Product = None):
        super().__init__(table)

        self.user: User = user
        self.date = date
        self.product: Product = product
