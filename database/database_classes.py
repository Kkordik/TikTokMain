import aiomysql
from aiomysql import Pool


class Database:
    def __init__(self, host: str, user: str, password: str,  name: str, pool: Pool = None, port: int = 3306):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__port = port

        self.__name = name
        self.__pool: Pool = pool

    async def make_pool(self, loop):
        self.__pool = await aiomysql.create_pool(host=self.__host, port=self.__port, user=self.__user,
                                                 password=self.__password, db=self.__name, autocommit=False, loop=loop)
        return self.__pool

    async def execute_db(self, command: str):
        """
        Execute any given command and return fetchall

        :param command: MySQL executable command
        :return: list of fetched rows
        """
        async with self.__pool.acquire() as con:
            async with con.cursor() as cur:
                await cur.execute(command)
                res = await cur.fetchall()
            await con.commit()
        return res

    async def _create_user_cl(self, new_usr_name: str, password: str):
        """create user for a client"""
        return await self.execute_db(f"CREATE USER '{new_usr_name}'@'%' IDENTIFIED BY '{password}';")

    async def _create_database_cl(self, new_db_name):
        """create db for a client"""
        await self.execute_db(f"CREATE SCHEMA '{new_db_name}';")

    async def _grant_privileges_cl(self, usr_name: str, new_db_name: str):
        """grant user clients privileges"""
        await self.execute_db(f"GRANT select ON tt_main_db.videos TO '{usr_name}'@'%';")
        return await self.execute_db(f"GRANT alter, create, delete, drop, execute, insert, select, update ON {new_db_name}.* TO"
                                     f" '{usr_name}'@'%';")

    async def _create_users_tb_cl(self):
        await self.execute_db(f"CREATE TABLE `{self.__name}`.`users` ("
                              "`id` SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT, `user_id` BIGINT NULL,"
                              " `active` TINYINT NULL DEFAULT 1, `date` DATE NULL,"
                              " PRIMARY KEY (`id`), UNIQUE INDEX `user_id_UNIQUE` (`user_id` ASC) VISIBLE);")

    async def launch_client_db(self, new_usr_name: str, new_password: str, new_db_name: str) -> Database:
        await self._create_user_cl(new_usr_name, new_password)
        await self._create_database_cl(new_db_name)
        await self._grant_privileges_cl(new_usr_name, new_db_name)
        client_db = Database(self.__host, new_usr_name, new_password, new_db_name)
        await client_db._create_users_tb_cl()
        # Here is left to create texts and urls tables, after it, I have to add purchase row to the main_db
        # call this method, copy client_bot, edit config and somehow run it all as task or process.
        #
        return client_db


class Table:
    def __init__(self, name: str, db: Database, columns: list):
        self.__name = name
        self.db = db
        self.__columns = columns

    async def execute_tb(self, command: str):
        """
        Execute any given command and return dict with values

        :param command: MySQL executable command
        :return: dict with values
        """
        res = await self.db.execute_db(command)
        results = []
        for row in res:
            results.append(dict(zip(self.__columns, row)))
        return results

    def __check_parameters(self, parameters: dict) -> dict[str: str]:
        """
        Checking if given columns in parameters dict exist in table.

        :param parameters: dict of structure {"column_name": value}
        :return: {"column_name": value}
        """
        for column in parameters.keys():
            # Checking if given columns in parameters exist in table and adding values to list
            if column in self.__columns:
                # Changing "string" to "'string'" to execute it in sql command as string
                if isinstance(parameters[column], str):
                    parameters[column] = "'{}'".format(parameters[column])
                else:
                    parameters[column] = str(parameters[column])
            else:
                raise Exception("In table '{}' is no such column: '{}'".format(self.__name, column))
        return parameters

    async def select_vals(self, command: str = "SELECT * FROM {}", logical_expr: str = "AND", **where):
        """
        Selects all from table can be executed with WHERE using AND or other logical_expression

        :param command: MySQL executable command
        :param logical_expr: logical expression 'AND'/'OR'...
        :param where: optional parameters for WHERE expression
        :return: dict with values if they are
        """
        where = self.__check_parameters(where)

        # Create string WHERE expression
        if len(where) != 0:
            where_str = "WHERE"
            where_equations = []
            for column in where.keys():
                where_equations.append(" {}={} ".format(column, where[column]))
            where_str += logical_expr.join(where_equations)
        else:
            where_str = ""

        return await self.execute_tb("{} {}".format(command.format(self.__name), where_str))

    async def delete_line(self, command: str = "DELETE FROM {}", logical_expr: str = "AND", **where):
        """
        Deletes all from table must be executed with WHERE, you may use AND or other logical_expression

        :param command: MySQL executable command
        :param logical_expr: logical expression 'AND'/'OR'...
        :param where: optional parameters for WHERE expression
        :return: dict with values if they are
        """
        where = self.__check_parameters(where)

        # Create string WHERE expression
        if len(where) != 0:
            where_str = "WHERE"
            where_equations = []
            for column in where.keys():
                where_equations.append(" {}={} ".format(column, where[column]))
            where_str += logical_expr.join(where_equations)
        else:
            raise Exception("No where arguments given. It is impossible to delete all from table")

        return await self.execute_tb("{} {}".format(command.format(self.__name), where_str))

    async def insert_vals(self, command: str = "INSERT IGNORE INTO {}({}) VALUES ({})", **columns_vals):
        """
        Insert values in table.

        :param columns_vals: parameters for INSERT must consist new data.
        :param command: MySQL command for inserting new values
        :return: list of fetched rows if they are
        """
        if len(columns_vals) == 0:
            raise Exception("No parameters given")

        columns_vals = self.__check_parameters(columns_vals)

        unpack_values = ', '.join(columns_vals.values())
        unpack_columns = ', '.join(columns_vals.keys())
        print(command.format(self.__name, unpack_columns, unpack_values))
        return await self.execute_tb(command.format(self.__name, unpack_columns, unpack_values))

    async def launch_table(self,  *args, **kwargs):
        pass

    async def update_val(self, *args, **kwargs):
        pass


class UsersTable(Table):
    """
    id: smallint unsigned auto_increment
    user_id: bigint
    start_date: date
    baned: tinyint(1)
    """
    __name = "users"
    __columns = ["id", "user_id", "start_date", "baned"]

    def __init__(self, db: Database):
        super().__init__(self.__name, db, self.__columns)


class VideosTable(Table):
    """
    id: smallint unsigned auto_increment
    video_dir: varchar(128)
    video_type: tinyint unsigned
    video_title: tinytext
    """
    __name = "videos"
    __columns = ["id", "video_dir", "video_type", "video_title"]

    def __init__(self, db: Database):
        self.db = db
        super().__init__(self.__name, self.db, self.__columns)


class ProductsTable(Table):
    """
    id: tinyint unsigned auto_increment
    prod_title: tinytext
    prod_price: smallint unsigned
    prod_descr: tinytext
    vid_amount: tinyint unsigned
    prod_photo: bigint
    """
    __name = "products"
    __columns = ["id", "prod_title", "prod_price", "prod_descr", "vid_amount", "prod_photo"]

    def __init__(self, db: Database):
        self.db = db
        super().__init__(self.__name, self.db, self.__columns)


class PurchasesTable(Table):
    """
    id: tinyint unsigned auto_increment
    user_id: smallint unsigned
    product_id: tinyint unsigned
    purchase_date: date
    """
    __name = "purchases"
    __columns = ["id", "user_id", "product_id", "purchase_date"]

    def __init__(self, db: Database):
        self.db = db
        super().__init__(self.__name, self.db, self.__columns)


class TextsTable(Table):
    """
    id: int unsigned auto_increment
    text_name: tinytext
    text: text
    language: tinytext
    """
    __name = "texts"
    __columns = ["id", "text_name", "text", "language"]

    def __init__(self, db: Database):
        self.db = db
        super().__init__(self.__name, self.db, self.__columns)
