# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asyncqlio/backends/base.py
# Compiled at: 2017-11-29 06:02:28
# Size of source mod 2**32: 9314 bytes
"""
The base implementation of a backend. This provides some ABC classes.
"""
import asyncio, collections, typing
from abc import abstractmethod
from collections import OrderedDict
from urllib.parse import ParseResult, parse_qs
from asyncqlio.meta import AsyncABC

class BaseDialect:
    __doc__ = '\n    The base class for a SQL dialect describer.\n\n    This class signifies what features the SQL dialect can use, and as such can be used to customize\n    query creation for faster results on certain servers, or new features on certain servers, etc.\n\n    By default, all ``has_`` properties will default to False, so that none of them need be\n    implemented. Regular methods will raise NotImplementedError, however.\n    '

    @property
    def has_checkpoints(self) -> bool:
        """
        Returns True if this dialect can use transaction checkpoints.
        """
        return False

    @property
    def has_serial(self) -> bool:
        """
        Returns True if this dialect can use the SERIAL datatype.
        """
        return False

    @property
    def has_returns(self) -> bool:
        """
        Returns True if this dialect has RETURNS.
        """
        return False

    @property
    def has_ilike(self) -> bool:
        """
        Returns True if this dialect has ILIKE.
        """
        return False

    @property
    def lastval_method(self):
        """
        The last value method for a dialect. For example, in PostgreSQL this is LASTVAL();
        """
        raise NotImplementedError


class BaseResultSet(collections.AsyncIterator, AsyncABC):
    __doc__ = '\n    The base class for a result set. This represents the results from a database query, as an async\n    iterable.\n\n    Children classes must implement:\n\n        - :attr:`.BaseResultSet.keys`\n        - :attr:`.BaseResultSet.fetch_row`\n        - :attr:`.BaseResultSet.fetch_many`\n    '

    @property
    @abstractmethod
    def keys(self) -> typing.Iterable[str]:
        """
        :return: An iterable of keys that this query contained.
        """
        pass

    @abstractmethod
    async def fetch_row(self) -> typing.Mapping[(str, typing.Any)]:
        """
        Fetches the **next row** in this query.

        This should return None if the row could not be fetched.
        """
        pass

    @abstractmethod
    async def fetch_many(self, n: int) -> typing.List[typing.Mapping[(str, typing.Any)]]:
        """
        Fetches the **next N rows** in this query.

        :param n: The number of rows to fetch.
        """
        pass

    @abstractmethod
    async def close(self):
        """
        Closes this result set.
        """
        pass

    async def __anext__(self):
        res = await self.fetch_row()
        if not res:
            raise StopAsyncIteration
        return res

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        return False


class BaseTransaction(AsyncABC):
    __doc__ = '\n    The base class for a transaction. This represents a database transaction (i.e SQL statements\n    guarded with a BEGIN and a COMMIT/ROLLBACK).\n\n    Children classes must implement:\n\n        - :meth:`.BaseTransaction.begin`\n        - :meth:`.BaseTransaction.rollback`\n        - :meth:`.BaseTransaction.commit`\n        - :meth:`.BaseTransaction.execute`\n        - :meth:`.BaseTransaction.cursor`\n        - :meth:`.BaseTransaction.close`\n\n    Additionally, some extra methods can be implemented:\n\n        - :meth:`.BaseTransaction.create_savepoint`\n        - :meth:`.BaseTransaction.release_savepoint`\n\n    These methods are not required to be implemented, but will raise :class:`NotImplementedError` if\n    they are not.\n\n    This class takes one parameter in the constructor: the :class:`.BaseConnector` used to connect\n    to the DB server.\n    '

    def __init__(self, connector: 'BaseConnector'):
        self.connector = connector

    async def __aenter__(self) -> 'BaseTransaction':
        await self.begin()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:
                await self.rollback()
                return False
            await self.commit()
            return False
        finally:
            await self.close()

    @abstractmethod
    async def begin(self):
        """
        Begins the transaction, emitting a BEGIN instruction.
        """
        pass

    @abstractmethod
    async def rollback(self, checkpoint: str=None):
        """
        Rolls back the transaction.

        :param checkpoint: If provided, the checkpoint to rollback to. Otherwise, the entire             transaction will be rolled back.
        """
        pass

    @abstractmethod
    async def commit(self):
        """
        Commits the current transaction, emitting a COMMIT instruction.
        """
        pass

    @abstractmethod
    async def execute(self, sql: str, params: typing.Union[(typing.Mapping, typing.Iterable)]=None):
        """
        Executes SQL in the current transaction.

        :param sql: The SQL statement to execute.
        :param params: Any parameters to pass to the query.
        """
        pass

    @abstractmethod
    async def close(self):
        """
        Called at the end of a transaction to cleanup.
        """
        pass

    @abstractmethod
    async def cursor(self, sql: str, params: typing.Union[(typing.Mapping, typing.Iterable)]=None) -> 'BaseResultSet':
        """
        Executes SQL and returns a database cursor for the rows.

        :param sql: The SQL statement to execute.
        :param params: Any parameters to pass to the query.
        :return: The :class:`.BaseResultSet` returned from the query, if applicable.
        """
        pass

    def create_savepoint(self, name: str):
        """
        Creates a savepoint in the current transaction.

        .. warning::
            This is not supported in all DB engines. If so, this will raise
            :class:`NotImplementedError`.

        :param name: The name of the savepoint to create.
        """
        raise NotImplementedError

    def release_savepoint(self, name: str):
        """
        Releases a savepoint in the current transaction.

        :param name: The name of the savepoint to release.
        """
        raise NotImplementedError


class BaseConnector(AsyncABC):
    __doc__ = '\n    The base class for a connector. This should be used for all connector classes as the parent\n    class.\n\n    Children classes must implement:\n\n        - :meth:`.BaseConnector.connect`\n        - :meth:`.BaseConnector.close`\n        - :meth:`.BaseConnector.emit_param`\n        - :meth:`.BaseConnector.get_transaction`\n        - :meth:`.BaseConnector.get_db_server_info`\n    '

    def __init__(self, dsn: ParseResult, *, loop: asyncio.AbstractEventLoop=None):
        """
        :param dsn: The :class:`urllib.parse.ParseResult` created from parsing a DSN.
        """
        self.loop = loop or asyncio.get_event_loop()
        self._parse_result = dsn
        self.dsn = dsn.geturl()
        self.host = dsn.hostname
        self.port = dsn.port
        self.username = dsn.username
        self.password = dsn.password
        self.db = dsn.path[1:]
        self.params = {k:v[0] for k, v in parse_qs(dsn.query).items()}

    @abstractmethod
    async def connect(self) -> 'BaseConnector':
        """
        Connects the current connector to the database server. This is called automatically by the
        :class:`.DatabaseInterface

        :return: The original BaseConnector instance.
        """
        pass

    @abstractmethod
    async def close(self):
        """
        Closes the current Connector.
        """
        pass

    @abstractmethod
    def get_transaction(self) -> BaseTransaction:
        """
        Gets a new transaction object for this connection.

        :return: A new :class:`~.BaseTransaction` object attached to this connection.
        """
        pass

    @abstractmethod
    def emit_param(self, name: str) -> str:
        """
        Emits a parameter that can be used as a substitute during a query.

        :param name: The name of the parameter.
        :return: A string that represents the substitute to be placed in the query.
        """
        pass

    @abstractmethod
    async def get_db_server_info(self):
        """
        :return: A :class:`.DBInfo` instance that contains information about the server.
        """
        pass


class DictRow(OrderedDict):
    __doc__ = '\n    Represents a row returned from a base result set, in dict form.\n\n    This class allows for accessing both via key and index.\n    '

    def __getitem__(self, item):
        if isinstance(item, int):
            try:
                return list(self.values())[item]
            except IndexError:
                raise KeyError(item)

        return super().__getitem__(item)

    def __setitem__(self, key, value, **kwargs):
        if isinstance(key, int):
            d_key = list(self.keys())[key]
            return (super().__setitem__)(d_key, value, **kwargs)
        else:
            return (super().__setitem__)(key, value, **kwargs)