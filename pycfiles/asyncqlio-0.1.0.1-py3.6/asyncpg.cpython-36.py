# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asyncqlio/backends/postgresql/asyncpg.py
# Compiled at: 2017-11-29 06:02:28
# Size of source mod 2**32: 6963 bytes
"""
The :ref:`asyncpg` connector for PostgreSQL databases.
"""
import asyncio, logging, typing, warnings, asyncpg
from asyncpg import Record
from asyncpg.cursor import Cursor
from asyncpg.transaction import Transaction
from asyncqlio.backends.base import BaseConnector, BaseResultSet, BaseTransaction, DictRow
from asyncqlio.exc import DatabaseException, IntegrityError, OperationalError
logger = logging.getLogger(__name__)

def get_param_query(sql: str, params: dict) -> typing.Tuple[(str, tuple)]:
    """
    Re-does a SQL query so that it uses asyncpg's special query format.

    :param sql: The SQL statement to use.
    :param params: The dict of parameters to use.
    :return: A two-item tuple of (new_query, arguments)
    """
    if not params or len(params) < 1:
        return (sql, ())
    else:
        kv = [(k, v) for k, v in params.items()]
        items = []
        fmt_dict = {}
        for n, (k, v) in enumerate(kv):
            n += 1
            fmt_dict[k] = '${}'.format(n)
            items.append(v)

        sql_statement = (sql.format)(**fmt_dict)
        return (
         sql_statement, tuple(items))


class AsyncpgResultSet(BaseResultSet):

    def __init__(self, cur: Cursor):
        self.cur = cur
        self._keys = None

    async def fetch_many(self, n: int):
        res = await self.cur.fetch(n)
        if res:
            if self._keys is None:
                self._keys = res[0].keys()
        return [DictRow(r) for r in res if r is not None]

    @property
    def keys(self) -> typing.Iterable[str]:
        if self._keys is None:
            raise RuntimeError('No keys have been fetched')
        return self._keys

    async def fetch_row(self):
        row = await self.cur.fetchrow()
        if self._keys is None:
            if row is not None:
                self._keys = row.keys()
        if row is not None:
            return DictRow(row)

    async def close(self):
        pass


class AsyncpgTransaction(BaseTransaction):
    __doc__ = '\n    A transaction that uses the `asyncpg <https://github.com/MagicStack/asyncpg>`_ library.\n    '

    def __init__(self, conn):
        super().__init__(conn)
        self.acquired_connection = None
        self.transaction = None

    async def begin(self, **transaction_options):
        """
        Begins the transaction.
        """
        logger.debug('Acquiring new transaction...')
        self.acquired_connection = await self.connector.pool.acquire()
        self.transaction = (self.acquired_connection.transaction)(**transaction_options)
        await self.transaction.start()
        logger.debug('Acquired and started transaction {}'.format(self.transaction))
        return self

    async def commit(self):
        """
        Commits the transaction.
        """
        await self.transaction.commit()

    async def rollback(self, checkpoint: str=None):
        if checkpoint is not None:
            await self.acquired_connection.execute('ROLLBACK TO {}'.format(checkpoint))
        else:
            await self.transaction.rollback()

    async def close(self):
        await self.connector.pool.release(self.acquired_connection)

    async def execute(self, sql: str, params: typing.Mapping[(str, typing.Any)]=None):
        """
        Executes SQL inside the transaction.

        :param sql: The SQL to execute.
        :param params: The parameters to excuse with.
        """
        logger.debug('Executing query {} with params {}'.format(sql, params))
        query, params = get_param_query(sql, params)
        try:
            results = await (self.acquired_connection.execute)(query, *params)
        except asyncpg.IntegrityConstraintViolationError as e:
            raise IntegrityError(*e.args) from e
        except asyncpg.ObjectNotInPrerequisiteStateError as e:
            raise OperationalError(*e.args) from e
        except asyncpg.SyntaxOrAccessError as e:
            raise DatabaseException(*e.args) from e

        return results

    async def cursor(self, sql: str, params: typing.Mapping[(str, typing.Any)]=None) -> AsyncpgResultSet:
        """
        Executes a SQL statement and returns a cursor to iterate over the rows of the result.
        """
        logger.debug('Transforming query {} with params {}'.format(sql, params))
        query, params = get_param_query(sql, params)
        logger.debug('Executing query {} with params {}'.format(query, params))
        cur = await (self.acquired_connection.cursor)(query, *params)
        result = AsyncpgResultSet(cur)
        return result

    async def create_savepoint(self, name: str):
        await self.acquired_connection.execute('SAVEPOINT {};'.format(name))

    async def release_savepoint(self, name: str):
        await self.acquired_connection.execute('RELEASE SAVEPOINT {};'.format(name))


class AsyncpgConnector(BaseConnector):
    __doc__ = '\n    A connector that uses the `asyncpg <https://github.com/MagicStack/asyncpg>`_ library.\n    '

    def __init__(self, parsed, *, loop=None):
        super().__init__(parsed, loop=loop)
        self.pool = None

    def __del__(self):
        if self.pool is not None:
            if not self.pool._closed:
                warnings.warn('Unclosed asyncpg pool {}'.format(self.pool))

    async def close(self):
        await self.pool.close()

    def emit_param(self, name: str) -> str:
        return '{{{name}}}'.format(name=name)

    async def connect(self) -> 'BaseConnector':
        port = self.port or 5432
        logger.debug('Connecting to {}'.format(self.dsn))
        self.pool = await (asyncpg.create_pool)(host=self.host, port=port, user=self.username, password=self.password, 
         database=self.db, loop=self.loop, **self.params)
        return self

    def get_transaction(self) -> 'AsyncpgTransaction':
        return AsyncpgTransaction(self)

    async def get_db_server_info(self):
        pass


CONNECTOR_TYPE = AsyncpgConnector