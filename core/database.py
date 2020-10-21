import asyncpg
from logging import debug
from typing import Union
from discord import User, Guild
#from datetime import datetime

class SQL:
    def __init__(self, pool: asyncpg.pool.Pool):
        """Requests to database.

        Arguments
        ---------
        pool: asyncpg.pool.Pool - Opened pool to DB
        """
        self.db = pool

    async def sql(self, code, *args):
        async with self.db.acquire() as connection:
            output = await connection.fetch(code, *args)
            await self.db.release(connection)
        debug(f'SQL Request {code} fetched')
        if len(output) == 1:
            return output[0]
        return output


    async def rawGetAll(self, table: str):
        """
        Gets all records from table.

        Arguments
        ---------
        table: str - Name of table
        """
        result = await self.sql(f"SELECT * FROM {table}") # nosec
        return result

    async def rawGet(self, table: str, column: str, value):
        """
        Gets records from database.

        Arguments
        ---------
        table: str - Name of table
        column: str - Column where will be check
        value - Value of column for check
        """
        result = await self.sql(f"SELECT * FROM {table} WHERE {column}=$1", value) # nosec
        return result

    async def rawDelete(self, table: str, column: str, value):
        """
        Deletes data from table.

        Arguments
        ---------
        table: str - Name of table
        column: str - Column where will be check
        value - Value of column for check
        """
        await self.sql(f"DELETE FROM {table} WHERE {column}=$1", value) # nosec

    async def rawWrite(self, table: str, *values):
        """
        Writes values.

        Arguments
        ---------
        table: str - Name of table
        *values - Values to record
        """
        args_description = ''
        for i in range(1, len(values)+1):
            args_description += f'${i}, ' if i != len(values) else f'${i}'
        await self.sql(f"INSERT INTO {table} VALUES ({args_description});", *values)

    async def rawUpdate(self, table: str, primary_key: str, update_params: str, *values):
        """
        Writes or updates values.

        Arguments
        ---------
        table: str - Name of table
        primary_key: str - Primary key, like 'id'
        update_params: str - Parameters for ON CONFLICT (primary_key) DO UPDATE SET ... Example - id=excluded.id
        returning: bool = False - Return recorded values?

        Returns
        ---------
        if returning==True
            asyncpg.Record of updated (created) row
        else
            Empty list
        """
        args_description = ''
    
        for i in range(1, len(values)+1): #  '$1, $2, $3'
            args_description += f'${i}, ' if i != len(values) else f'${i}'

        request = f"INSERT INTO {table} VALUES ({args_description}) ON CONFLICT ({primary_key}) DO UPDATE SET {update_params} RETURNING *" # nosec
        return await self.sql(request, *values)


class PrefixesSQL(SQL):
    """Requests to DB associated with prefixes.

    Arguments
    ---------
    pool: asyncpg.pool.Pool - Opened pool to DB
    config: dict - Bot config
    """
    def __init__(self, pool: asyncpg.pool.Pool, config: dict):
        super().__init__(pool)
        self.standartValue = config["prefix"]

    async def get(self, obj: Union[User, Guild]) -> str:
        """
        Get user/guild's prefix from DB.

        Arguments
        ---------
        obj: discord.User or discord.Guild
        """
        _id = obj.id

        result = await self.rawGet(table="prefixes", column="id", value=_id)

        prefix = result.get("value") if not isinstance(result, list) else None
        # .get is dict function,
        # if value not recorded in table self.sql returns [], so we cannot use .get
        return prefix

    async def set(self, obj: Union[User, Guild], value: str=None) -> None:
        """
        Sets user/guild prefix.

        Arguments
        ---------
        obj: discord.User or discord.Guild
        value: str = None - new prefix. Leave blank for delete
        """
        _id = obj.id
        if not value:
            await self.rawDelete('prefixes', 'id', _id)
        await self.rawUpdate('prefixes', 'id', 'value=EXCLUDED.value', _id, value) # table=prefixes, primary_key=_id, update_params='value=EXCLUDED.value'

    async def reset(self, obj: Union[User, Guild]) -> None:
        """await .set(obj) alias."""
        await self.set(obj)
        
class LocaleSQL(SQL):
    """Requests to DB associated with locale.

    Arguments
    ---------
    pool: asyncpg.pool.Pool - Opened pool to DB
    config: dict - Bot config
    """
    def __init__(self, pool: asyncpg.pool.Pool, config: dict):
        self.db = pool
        self.baseLanguage = config['locale.base']

    async def get(self, obj: Union[User, Guild]) -> str:
        """
        Get user/guild's locale from DB.

        Arguments
        ---------
        obj: discord.User or discord.Guild
        """
        _id = obj.id

        result = await self.rawGet(table="locale", column="id", value=_id)

        prefix = result.get("value") if not isinstance(result, list) else self.baseLanguage
        # .get is dict function,
        # if value not recorded in table self.sql returns [], so we cannot use .get
        return prefix

    async def set(self, obj: Union[User, Guild], value: str) -> None:
        """
        Sets user/guild locale.

        Arguments
        ---------
        obj: discord.User or discord.Guild
        value: str - new locale
        """
        _id = obj.id

        await self.rawUpdate('locale', 'id', 'value=EXCLUDED.value', _id, value) # table=prefixes, primary_key=_id, update_params='value=EXCLUDED.value'
    


CREATE_TABLES = (
    """CREATE TABLE IF NOT EXISTS locale (
        id bigint CHECK (id > 0) PRIMARY KEY,
        value varchar(8)
    );""",
    """CREATE TABLE IF NOT EXISTS prefixes (
        id bigint CHECK (id > 0) PRIMARY KEY,
        value varchar(7)
    );"""
    )