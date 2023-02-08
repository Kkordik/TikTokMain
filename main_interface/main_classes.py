from typing import Union

from database.database_classes import Table, UsersTable, PurchasesTable, ProductsTable, VideosTable, TextsTable
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
        self._language = language
        self.purchases = purchases
        self.baned = baned

    async def __get_row_id(self):
        self.row_id = await self.table.select_vals(user_id=self.user_id)["id"]
        return self.row_id

    async def insert_user(self, user_id=None):
        if user_id:
            self.user_id = int(user_id)
        return await self.table.insert_vals(user_id=int(self.user_id))

    def language(self):
        return self._language


class Video(MainClassBase):
    def __init__(self, table: VideosTable, row_id: int = None, video_id=None, video_dir: str = None,
                 video_type: int = None, video_title: str = None):
        super().__init__(table, row_id)

        self.video_id = int(video_id)
        self.video_dir = video_dir
        self.video_type = video_type
        self.video_title = video_title


class Product(MainClassBase):
    def __init__(self, table: ProductsTable, row_id: int = None, title: str = None, price: int = None,
                 description: str = None, vid_amount: int = None, prod_photo_id: int = None):
        super().__init__(table, row_id)

        self.title = title
        self.price = price
        self.description = description
        self.vid_amount = vid_amount
        self.prod_photo_id = prod_photo_id

    def check_full_filling(self) -> bool:
        if self.title and self.price and self.vid_amount and self.prod_photo_id:
            return True
        else:
            return False

    async def get_all_products(self) -> dict:
        prods_list = {}
        for prod in await self.table.select_vals():
            prods_list[prod["id"]] = Product(self.table, row_id=prod["id"], title=prod["prod_title"],
                                             price=prod["prod_price"], description=prod["prod_descr"],
                                             vid_amount=prod["vid_amount"], prod_photo_id=prod["prod_photo"])
        return prods_list


class Purchase(MainClassBase):
    def __init__(self, table: PurchasesTable, row_id: int = None, user: User = None, date: str = "",
                 product: Product = None):
        super().__init__(table, row_id)

        self.user: User = user
        self.date = date
        self.product: Product = product


class Text(MainClassBase):
    def __init__(self, table: TextsTable, row_id: int = None, text_name: str = None, text: str = None,
                 language: str = None):
        super().__init__(table, row_id)

        self.text_name = text_name
        self.text = text
        self.language = language

    async def get_texts(self, language: str = None, text_name: str = None) -> []:
        """
        Get all texts defined by text_name and language(can be None)
        :param language:
        :param text_name:
        :return: list Text objects
        """
        if text_name:
            self.text_name = text_name

        if language:
            self.language = language

        texts = []
        if self.language:
            for text in await self.table.select_vals(language=self.language, text_name=self.text_name):
                texts.append(Text(self.table, text_name=text["text_name"], text=text["text"],
                                  language=text["language"]))
        else:
            for text in await self.table.select_vals(text_name=self.text_name):
                texts.append(Text(self.table, text_name=text["text_name"], text=text["text"],
                                  language=text["language"]))
        return texts

    async def get_const_text(self, language, text_name: str = None) -> str:
        """
        Get constant text from database.
        :param language:
        :param text_name:
        :return: str (text of first returned object from db)
        """
        res = await self.get_texts(language, text_name)
        self.text = res[0].text
        return self.text
