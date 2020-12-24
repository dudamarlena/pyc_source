# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/lead/interfaces.py
# Compiled at: 2008-04-27 07:30:45
from zope.interface import Interface, Attribute

class IDatabase(Interface):
    """A database connection, lazily instantiating an SQLAlchemy engine.
    The engine is threadlocal, and its transactions are tied to Zope
    transactions.
    """
    __module__ = __name__
    session = Attribute('An SQLAlchemy session. Use this for ORM session operations.')
    connection = Attribute('An SQLAlchemy connection. Use this to execute SQL.')
    engine = Attribute('The underlying engine object. This uses a threadlocal strategy.')
    tables = Attribute("A dictionary of SQLAlchemy Table's, keyed by table name, for this database")
    mappers = Attribute("A dictionary of SQLAlchemy Mapper's, keyed by entity name, for this database")


class IConfigurableDatabase(IDatabase):
    """Configuration aspects of an IDatabase
    """
    __module__ = __name__

    def invalidate(self):
        """Invalidate the configuration of the database, causing the engine
        to be re-initialised. This will not re-map database tables 
        (self._setup_tables() and self._setup_mappers() are still called at
        most once per Zope start-up), but tables will be re-bound to 
        different metadata if necessary.
        """
        pass

    _url = Attribute('An sqlalchemy.engine.url.URL used to connect to the database server')
    _engine_properties = Attribute('A dictionary of additional arguments to pass to create_engine()')

    def _setup_tables(metadata, tables):
        """Given an SQLAlchemy Metadata for the current engine, set up
        Tables for the database structure, saving them to the dict
        'tables', keyed by table name.
        """
        pass

    def _setup_mappers(tables, mappers):
        """Given a dict of tables, keyed by table name as in self.tables,
        set up all SQLAlchemy mappers for the database and save them to the
        dict 'mappers', keyed by table name..
        """
        pass


class ITransactionAware(Interface):
    """Transaction-aware objects
    """
    __module__ = __name__

    def begin():
        """Begin the transaction
        """
        pass

    def commit():
        """Commit the transaction
        """
        pass

    def rollback():
        """Commit the transaction
        """
        pass

    active = Attribute('True if the transaction is currently in-progress')