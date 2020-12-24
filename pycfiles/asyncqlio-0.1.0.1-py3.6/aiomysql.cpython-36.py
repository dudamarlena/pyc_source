# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asyncqlio/backends/mysql/aiomysql.py
# Compiled at: 2017-11-29 06:02:28
# Size of source mod 2**32: 5084 bytes
"""
The :ref:`aiomysql` connector for MySQL/MariaDB databases.
"""
import logging, typing, aiomysql, pymysql
from asyncqlio.backends.base import BaseConnector, BaseResultSet, BaseTransaction, DictRow
logger = logging.getLogger(__name__)
aiomysql.DictCursor.dict_type = DictRow

class AiomysqlResultSet(BaseResultSet):
    __doc__ = '\n    Represents a result set returned by the MySQL database.\n    '

    def __init__(self, cursor: aiomysql.DictCursor):
        self.cursor = cursor
        self._keys = None

    @property
    def keys(self):
        return self._keys

    async def close(self):
        return await self.cursor.close()

    async def fetch_row(self) -> typing.Dict[(typing.Any, typing.Any)]:
        """
        Fetches the next row in this result set.
        """
        row = await self.cursor.fetchone()
        if self._keys is None:
            if row is not None:
                self._keys = row.keys()
        return row

    async def fetch_many(self, n: int):
        """
        Fetches the next N rows.
        """
        return await self.cursor.fetchmany(size=n)

    async def fetch_all(self):
        """
        Fetches ALL the rows.
        """
        return await self.cursor.fetchall()


class AiomysqlTransaction(BaseTransaction):
    __doc__ = '\n    Represents a transaction for aiomysql.\n    '

    def __init__(self, connector):
        super().__init__(connector)
        self.connection = None

    async def close(self):
        """
        Closes the current connection.
        """
        self.connector.pool.release(self.connection)

    async def begin(self):
        """
        Begins the current transaction.
        """
        self.connection = await self.connector.pool.acquire()
        await self.connection.begin()
        return self

    async def execute(self, sql: str, params: typing.Union[(typing.Mapping, typing.Iterable)]=None):
        """
        Executes some SQL in the current transaction.
        """
        cursor = await self.connection.cursor(cursor=(aiomysql.DictCursor))
        res = await cursor.execute(sql, params)
        await cursor.close()
        return res

    async def cursor(self, sql: str, params: typing.Union[(typing.Mapping, typing.Iterable)]=None) -> 'AiomysqlResultSet':
        """
        Returns a :class:`.AiomysqlResultSet` for the specified SQL.
        """
        cursor = await self.connection.cursor(cursor=(aiomysql.DictCursor))
        await cursor.execute(sql, params)
        return AiomysqlResultSet(cursor)

    async def rollback(self, checkpoint: str=None):
        """
        Rolls back the current transaction.

        :param checkpoint: Ignored.
        """
        await self.connection.rollback()

    async def commit(self):
        """
        Commits the current transaction.
        """
        await self.connection.commit()


class AiomysqlConnector(BaseConnector):
    __doc__ = '\n    A connector that uses the `aiomysql <https://github.com/aio-libs/aiomysql>`_ library.\n    '

    def __init__(self, dsn, *, loop=None):
        super().__init__(dsn, loop=loop)
        self.pool = None

    async def connect(self) -> 'AiomysqlConnector':
        """
        Connects this connector.
        """
        port = self.port or 3306
        logger.info('Connecting to MySQL on mysql://{}:{}/{}'.format(self.host, port, self.db))
        self.pool = await (aiomysql.create_pool)(host=self.host, user=self.username, password=self.password, 
         port=port, db=self.db, **self.params)
        return self

    async def close(self, forcefully: bool=False):
        """
        Closes this connector.
        """
        if forcefully:
            await self.pool.terminate()
        else:
            await self.pool.close()
            await self.pool.wait_closed()

    def get_transaction(self) -> BaseTransaction:
        """
        Gets a new transaction object.
        """
        return AiomysqlTransaction(self)

    def emit_param(self, name: str) -> str:
        if pymysql.paramstyle == 'pyformat':
            return '%({})s'.format(name)
        if pymysql.paramstyle == 'named':
            return ':{}'.format(name)
        raise ValueError('Cannot work with paramstyle {}'.format(pymysql.paramstyle))

    def get_db_server_info(self):
        pass


CONNECTOR_TYPE = AiomysqlConnector