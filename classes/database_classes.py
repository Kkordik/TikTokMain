import aiomysql
import asyncio
from aiomysql import Pool


class Database:
    def __init__(self, host: str, user: str, password: str,  name: str, port: int = 22):
        self.host = host
        self.user = user
        self.password = password
        self.port = port

        self.name = name
        self.pool: Pool = None

    async def make_pool(self, loop):
        self.pool = await aiomysql.create_pool(host=self.host, port=self.port, user=self.user, password=self.password,
                                               db=self.name, autocommit=False, loop=loop)
        return self.pool

# Execute any given command and return fetchall
    async def execute_db(self, command):
        async with self.pool.acquire() as con:
            async with con.cursor() as cur:
                res = await cur.execute(command)
            await con.commit()
        # return await res.fetchall()
        return res


class Table:
    def __init__(self, name: str, db: Database):
        self.name = name
        self.db = db

    async def select_all(self, command: str = "SELECT * FROM {}", where: str = ""):
        if where:
            where = "WHERE " + where
        print("{} {}".format(command.format(self.name), where))
        return await self.db.execute_db("{} {}".format(command.format(self.name), where))

    async def insert_vals(self, *args, **kwargs):
        pass

    async def execute_tb(self, command):
        return await self.db.execute_db(command)

    async def launch_table(self):
        pass

    async def update_val(self, *args, **kwargs):
        pass


class UsersTable(Table):
    """
    id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNIQUE,
    start_date DATE,
    baned BOOLEAN DEFAULT 0
    """
    __name = "users"
    __columns = {"id", "user_id", "start_date", "baned"}

    def __init__(self, db: Database):
        self.db = db
        super().__init__(self.__name, self.db)

    async def insert_vals(self, command: str = "INSERT IGNORE INTO {}({}) VALUES ({})", **columns_vals):
        unpack_columns = []
        unpack_values = []

        # Checking if given columns exist in table and adding values to list
        for column in columns_vals.keys():
            if column in self.__columns:
                unpack_columns.append(column)
                unpack_values.append(str(columns_vals[column]))
            else:
                raise Exception("In table is no such column: '{}'".format(column))
        unpack_values = ', '.join(unpack_values)
        unpack_columns = ', '.join(unpack_columns)

        return await self.db.execute_db(command.format(self.__name, unpack_columns, unpack_values))


