# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asyncqlio/db.py
# Compiled at: 2017-11-29 06:02:28
# Size of source mod 2**32: 5267 bytes
"""
The main Database object. This is the "database interface" to the actual DB server.
"""
import asyncio, importlib, logging
from urllib.parse import ParseResult, urlparse
from asyncqlio.backends.base import BaseConnector, BaseDialect, BaseTransaction
from asyncqlio.orm import session as md_session
from asyncqlio.orm.schema import table as md_table
NO_CONNECTOR = object()
logger = logging.getLogger('asyncqlio')

class DatabaseInterface(object):
    __doc__ = '\n    The "database interface" to your database. This provides the actual connection to the DB server,\n    including things such as querying, inserting, updating, et cetera.\n\n    Creating a new database object is simple:\n\n    .. code-block:: python3\n\n        # pass the DSN in the constructor\n        dsn = "postgresql://postgres:B07_L1v3s_M4tt3r_T00@127.0.0.1/mydb"\n        my_database = DatabaseInterface(dsn)\n        # or provide it in the `.connect()` call\n        await my_database.connect(dsn)\n\n    '

    def __init__(self, dsn: str=None, *, loop: asyncio.AbstractEventLoop=None):
        """
        :param dsn:
            The `Data Source Name <http://whatis.techtarget.com/definition/data-source-name-DSN>_`
            to connect to the database on.
        """
        self._dsn = dsn
        self.loop = loop or asyncio.get_event_loop()
        self.connector = None
        self.dialect = None

    async def __aenter__(self):
        if not self.connected:
            await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        return False

    @property
    def connected(self):
        """
        Checks if this DB is connected.
        """
        return self.connector is not None

    def bind_tables(self, md: 'md_table.TableMetadata'):
        """
        Binds tables to this DB instance.
        """
        if isinstance(md, md_table.TableMeta):
            md = md.metadata
        md._bind = self
        md.setup_tables()
        return md

    async def connect(self, dsn: str=None, **kwargs) -> BaseConnector:
        """
        Connects the interface to the database server.

        .. note::
            For SQLite3 connections, this will just open the database for reading.

        :param dsn: The Data Source Name to connect to, if it was not specified in the constructor.
        :return: The :class:`~.BaseConnector` established.
        """
        if dsn is not None:
            self._dsn = dsn
        else:
            parsed_dsn = urlparse(self._dsn)
            schemes = parsed_dsn.scheme.split('+')
            db_type = schemes[0]
            try:
                db_connector = schemes[1]
            except IndexError:
                db_connector = NO_CONNECTOR

            import_path = 'asyncqlio.backends.{}'.format(db_type)
            package = importlib.import_module(import_path)
            if db_connector is not NO_CONNECTOR:
                mod_path = '.'.join([import_path, db_connector])
            else:
                mod_path = '.'.join([import_path, package.DEFAULT_CONNECTOR])
        self.dialect = getattr(package, '{}Dialect'.format(db_type.title()))()
        logger.debug('Loading connector {}'.format(mod_path))
        connector_mod = importlib.import_module(mod_path)
        connector_ins = connector_mod.CONNECTOR_TYPE(parsed_dsn,
          loop=(self.loop))
        self.connector = connector_ins
        try:
            await (self.connector.connect)(**kwargs)
        except Exception:
            self.connector = None
            raise

        return self.connector

    def emit_param(self, name: str) -> str:
        """
        Emits a param in the format that the DB driver specifies.

        :param name: The name of the parameter to emit.
        :return: A str representing the emitted param.
        """
        return self.connector.emit_param(name)

    def get_transaction(self, **kwargs) -> BaseTransaction:
        """
        Gets a low-level :class:`.BaseTransaction`.

        .. code-block:: python3

            async with db.get_transaction() as transaction:
                results = await transaction.cursor("SELECT 1;")
        """
        return (self.connector.get_transaction)(**kwargs)

    def get_session(self, **kwargs) -> 'md_session.Session':
        """
        Gets a new :class:`.Session` bound to this instance.
        """
        return (md_session.Session)(self, **kwargs)

    async def close(self):
        """
        Closes the current database interface.
        """
        if self.connector is not None:
            await self.connector.close()

    async def get_db_server_info(self):
        """
        Gets DB server info.

        .. warning::
            This is **not** supported on SQLite3 connections.
        """
        pass