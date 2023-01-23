from database.database_classes import Table, UsersTable, PurchasesTable, ProductsTable
from config import BASIC_LANGUAGE


class MainClassBase:
    def __init__(self, table, row_id: int = None):
        self.table: Table = table
        self.row_id = row_id


class User(MainClassBase):
    def __init__(self, table: UsersTable, user_id, row_id: int = None, language: str = BASIC_LANGUAGE,
                 purchases: [] = None, baned: bool = None):
        super().__init__(table, row_id)

        self.user_id: int = int(user_id)
        self.language = language
        self.purchases = purchases
        self.baned = baned

    async def __get_row_id(self):
        self.row_id = await self.table.select_vals(user_id=self.user_id)["id"]
        return self.row_id

    async def insert_user(self, user_id=None):
        if user_id:
            self.user_id = int(user_id)
        return await self.table.insert_vals(user_id=int(self.user_id))


class Product(MainClassBase):
    def __init__(self, table: ProductsTable, row_id: int = None, title: str = None, price: int = None, description: str = None,
                 vid_amount: int = None, prod_photo_id: int = None):
        super().__init__(table, row_id)

        self.title = title
        self.price = price
        self.description = description
        self.vid_amount = vid_amount
        self.prod_photo_id = prod_photo_id

    async def get_all_products(self) -> []:
        prods_list = []
        for prod in await self.table.select_vals():
            prods_list.append(Product(self.table, row_id=prod["id"], title=prod["prod_title"], price=prod["prod_price"],
                                      description=prod["prod_descr"], vid_amount=prod["vid_amount"],
                                      prod_photo_id=prod["prod_photo"]))
        return prods_list


class Purchase(MainClassBase):
    def __init__(self, table: PurchasesTable, row_id: int = None, user: User = None, date: str = "", product: Product = None):
        super().__init__(table, row_id)

        self.user: User = user
        self.date = date
        self.product: Product = product
