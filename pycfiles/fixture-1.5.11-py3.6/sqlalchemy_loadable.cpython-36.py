# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fixture/loadable/sqlalchemy_loadable.py
# Compiled at: 2017-10-02 03:31:12
# Size of source mod 2**32: 14467 bytes
"""Components for loading and unloading data using `SQLAlchemy`_.

See :ref:`Using LoadableFixture<using-loadable-fixture>` for examples.

.. _SQLAlchemy: http://www.sqlalchemy.org/

"""
import sys
from fixture.loadable import DBLoadableFixture
from fixture.exc import UninitializedError
import logging
log = logging.getLogger('fixture.loadable.sqlalchemy_loadable')
try:
    from sqlalchemy.orm import sessionmaker, scoped_session
except ImportError:
    Session = None
    sa_major = None
else:
    import sqlalchemy
    sa_major = float(sqlalchemy.__version__[:3])
    if sa_major < 0.5:
        Session = scoped_session(sessionmaker(autoflush=False, transactional=True), scopefunc=(lambda : __name__))
    else:
        Session = scoped_session(sessionmaker(autoflush=False, autocommit=False), scopefunc=(lambda : __name__))

    def negotiated_medium(obj, dataset):
        if is_table(obj):
            return TableMedium(obj, dataset)
        else:
            if is_assigned_mapper(obj):
                return MappedClassMedium(obj, dataset)
            if is_mapped_class(obj):
                return MappedClassMedium(obj, dataset)
        raise NotImplementedError('object %s is not supported by %s' % (
         obj, SQLAlchemyFixture))


    class SQLAlchemyFixture(DBLoadableFixture):
        __doc__ = '\n    A fixture that knows how to load DataSet objects into `SQLAlchemy`_ objects.\n    \n    >>> from fixture import SQLAlchemyFixture\n    \n    The recommended way to deal with connections is to either pass in your own engine object \n    or let `implicit binding`_ govern how connections are made.  This is because \n    ``SQLAlchemyFixture`` will use an internally scoped session to avoid conflicts \n    with that of the Application Under Test.  If you need to bypass this behavior then \n    pass in your own session or scoped_session.\n    \n    For examples of usage see :ref:`Using LoadableFixture <using-loadable-fixture>`\n    \n    .. _implicit binding: http://www.sqlalchemy.org/docs/04/dbengine.html#dbengine_implicit\n    \n    Keyword Arguments:\n    \n    ``style``\n        A :class:`Style <fixture.style.Style>` object to translate names with\n    \n    ``env``\n        A dict or module that contains either mapped classes or Table objects,\n        or both.  This will be searched when :class:`Style <fixture.style.Style>` \n        translates DataSet names into\n        storage media.  See :meth:`EnvLoadableFixture.attach_storage_medium <fixture.loadable.loadable.EnvLoadableFixture.attach_storage_medium>` for details on \n        how ``env`` works.\n    \n    ``engine``\n        A specific connectable/engine object to use when one is not bound.  \n        engine.connect() will be called.\n    \n    ``session``\n        A session from ``sqlalchemy.create_session()``.  See `Contextual/Thread-local Sessions`_\n        for more info.  This will override the \n        ScopedSession and SessionContext approaches.  Only declare a session if you have to.  \n        The preferred way is to let fixture use its own session in a private scope.\n    \n    .. _Contextual/Thread-local Sessions: http://www.sqlalchemy.org/docs/04/session.html#unitofwork_contextual\n    \n    ``scoped_session``\n        A class-like ``Session`` object created by ``scoped_session(sessionmaker())``.  \n        Only declare a custom Session if you have to.  The preferred way \n        is to let fixture use its own Session which defines a private scope to \n        avoid conflicts with that of the Application Under Test.\n    \n    ``connection``\n        A specific connection / engine to use when one is not bound.\n    \n    ``dataclass``\n        :class:`SuperSet <fixture.dataset.SuperSet>` class to represent loaded data with\n    \n    ``medium``\n        A custom :class:`StorageMediumAdapter <fixture.loadable.loadable.StorageMediumAdapter>` \n        to instantiate when storing a DataSet.\n        By default, a medium adapter will be negotiated based on the type of \n        SQLAlchemy object so you should only set this if you know what you \n        doing.\n    \n    '
        Medium = staticmethod(negotiated_medium)

        def __init__(self, engine=None, connection=None, session=None, scoped_session=None, **kw):
            from sqlalchemy.orm import sessionmaker, scoped_session as sa_scoped_session
            (DBLoadableFixture.__init__)(self, **kw)
            self.engine = engine
            self.connection = connection
            self.session = session
            if scoped_session is None:
                scoped_session = Session
            self.Session = scoped_session

        def begin(self, unloading=False):
            """Begin loading data
        
        - creates and stores a connection with engine.connect() if an engine was passed
          
          - binds the connection or engine to fixture's internal session
          
        - uses an unbound internal session if no engine or connection was passed in
        """
            if not unloading:
                Session.remove()
            elif self.connection is None:
                if self.engine is None:
                    if self.session:
                        self.engine = self.session.bind
            else:
                if self.engine is not None:
                    if self.connection is None:
                        self.connection = self.engine.connect()
                if self.session is None:
                    if self.connection:
                        self.session = self.Session(bind=(self.connection))
                    else:
                        self.session = self.Session(bind=None)
            DBLoadableFixture.begin(self, unloading=unloading)

        def commit(self):
            """Commit the load transaction and flush the session
        """
            if self.connection:
                self.session.flush()
            log.debug('transaction.commit() <- %s', self.transaction)
            DBLoadableFixture.commit(self)

        def create_transaction(self):
            """Create a session transaction or a connection transaction
        
        - if a custom connection was used, calls connection.begin
        - otherwise calls session.begin()
        
        """
            if self.connection is not None:
                log.debug('connection.begin()')
                transaction = self.connection.begin()
            else:
                transaction = self.session.begin()
            log.debug('create_transaction() <- %s', transaction)
            return transaction

        def dispose(self):
            """Dispose of this fixture instance entirely
        
        Closes all connection, session, and transaction objects and calls engine.dispose()
        
        After calling fixture.dispose() you cannot use the fixture instance.  
        Instead you have to create a new instance like::
        
            fixture = SQLAlchemyFixture(...)
        
        """
            from fixture.dataset import dataset_registry
            dataset_registry.clear()
            if self.connection:
                self.connection.close()
            if self.session:
                self.session.close()
            if self.transaction:
                self.transaction.close()
            if self.engine:
                self.engine.dispose()

        def rollback(self):
            """Rollback load transaction"""
            DBLoadableFixture.rollback(self)


    class MappedClassMedium(DBLoadableFixture.StorageMediumAdapter):
        __doc__ = '\n    Adapter for `SQLAlchemy`_ mapped classes.\n    \n    For example, in ``mapper(TheClass, the_table)`` ``TheClass`` is a mapped class.\n    If using `Elixir`_ then any class descending from ``elixir.Entity`` is treated like a mapped class.\n    \n    .. _Elixir: http://elixir.ematia.de/\n    \n    '

        def __init__(self, *a, **kw):
            (DBLoadableFixture.StorageMediumAdapter.__init__)(self, *a, **kw)

        def clear(self, obj):
            """Delete this object from the session"""
            self.session.delete(obj)

        def visit_loader(self, loader):
            """Visits the :class:`SQLAlchemyFixture` loader and stores a reference to its session"""
            self.session = loader.session

        def save(self, row, column_vals):
            """Save a new object to the session if it doesn't already exist in the session."""
            obj = self.medium()
            for c, val in column_vals:
                setattr(obj, c, val)

            if obj not in self.session.new:
                if hasattr(self.session, 'add'):
                    self.session.add(obj)
                else:
                    self.session.save(obj)
            return obj


    class LoadedTableRow(object):

        def __init__(self, table, inserted_key, conn):
            self.table = table
            self.conn = conn
            self.inserted_key = [k for k in inserted_key]
            self.row = None

        def __getattr__(self, col):
            if not self.row:
                if len(self.inserted_key) > 1:
                    raise NotImplementedError('%s does not support making a select statement with a composite key, %s.  This is probably fixable' % (
                     self.__class__.__name__,
                     self.table.primary_key))
                else:
                    first_pk = [k for k in self.table.primary_key][0]
                    id = getattr(self.table.c, first_pk.key)
                    stmt = self.table.select(id == self.inserted_key[0])
                    if self.conn:
                        c = self.conn.execute(stmt)
                    else:
                        c = stmt.execute()
                self.row = c.fetchone()
            return getattr(self.row, col)


    class TableMedium(DBLoadableFixture.StorageMediumAdapter):
        __doc__ = '\n    Adapter for `SQLAlchemy Table objects`_\n    \n    If no connection or engine is configured in the :class:`SQLAlchemyFixture` \n    then statements will be executed directly on the Table object itself which adheres \n    to `implicit connection rules`_.  Otherwise, \n    the respective connection or engine will be used to execute statements.\n    \n    .. _SQLAlchemy Table objects: http://www.sqlalchemy.org/docs/04/ormtutorial.html#datamapping_tables\n    .. _implicit connection rules: http://www.sqlalchemy.org/docs/04/dbengine.html#dbengine_implicit\n    \n    '

        def __init__(self, *a, **kw):
            (DBLoadableFixture.StorageMediumAdapter.__init__)(self, *a, **kw)
            self.conn = None

        def clear(self, obj):
            """Constructs a delete statement per each primary key and 
        executes it either explicitly or implicitly
        """
            i = 0
            for k in obj.table.primary_key:
                id = getattr(obj.table.c, k.key)
                stmt = obj.table.delete(id == obj.inserted_key[i])
                if self.conn:
                    c = self.conn.execute(stmt)
                else:
                    c = stmt.execute()
                i += 1

        def visit_loader(self, loader):
            """Visits the :class:`SQLAlchemyFixture` loader and stores a reference 
        to its connection if there is one.
        """
            if loader.connection:
                self.conn = loader.connection
            else:
                self.conn = None

        def save(self, row, column_vals):
            """Constructs an insert statement with the given values and 
        executes it either explicitly or implicitly
        """
            from sqlalchemy.schema import Table
            if not isinstance(self.medium, Table):
                raise ValueError('medium %s must be a Table instance' % self.medium)
            else:
                stmt = self.medium.insert()
                params = dict(list(column_vals))
                if self.conn:
                    c = self.conn.execute(stmt, params)
                else:
                    c = stmt.execute(params)
                if hasattr(c, 'primary_key'):
                    primary_key = c.primary_key
                else:
                    primary_key = c.last_inserted_ids()
            if primary_key is None:
                raise NotImplementedError('what can we do with a None primary key?')
            table_keys = [k for k in self.medium.primary_key]
            inserted_keys = [k for k in primary_key]
            if len(inserted_keys) != len(table_keys):
                raise ValueError('expected primary_key %s, got %s (using table %s)' % (
                 table_keys, inserted_keys, self.medium))
            return LoadedTableRow(self.medium, primary_key, self.conn)


    def is_assigned_mapper(obj):
        import sqlalchemy
        if sa_major <= 0.3:
            from sqlalchemy.orm.mapper import Mapper

            def is_assigned(obj):
                return hasattr(obj, 'mapper') and isinstance(obj.mapper, Mapper)

        else:
            if sa_major < 0.5:
                from sqlalchemy import exceptions as sqlalchemy_exc
            else:
                from sqlalchemy import exc as sqlalchemy_exc
            from sqlalchemy.orm.mapper import class_mapper

            def is_assigned(obj):
                try:
                    cm = class_mapper(obj)
                except sqlalchemy_exc.InvalidRequestError:
                    return False
                else:
                    return True

        return is_assigned(obj)


    def is_mapped_class(obj):
        if sa_major < 0.5:
            from sqlalchemy import util
            return hasattr(obj, 'c') and isinstance(obj.c, util.OrderedProperties)
        else:
            return hasattr(obj, '_sa_class_manager')


    def is_table(obj):
        from sqlalchemy.schema import Table
        return isinstance(obj, Table)