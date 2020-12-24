# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fixture/loadable/sqlobject_loadable.py
# Compiled at: 2017-10-02 03:31:12
# Size of source mod 2**32: 4059 bytes
"""Components for loading and unloading data using `SQLObject`_.

See :ref:`Using LoadableFixture<using-loadable-fixture>` for examples.

.. _SQLObject: http://www.sqlobject.org/

"""
from fixture.loadable import DBLoadableFixture

class SQLObjectMedium(DBLoadableFixture.StorageMediumAdapter):
    __doc__ = '\n    Adapter for storing data using `SQLObject`_ classes\n    '

    def clear(self, obj):
        """Delete this object from the DB"""
        obj.destroySelf()

    def save(self, row, column_vals):
        """Save this row to the DB"""
        from sqlobject.styles import getStyle
        so_style = getStyle(self.medium)
        if hasattr(row, 'connection'):
            raise ValueError("cannot name a key 'connection' in row %s" % row)
        dbvals = dict([(so_style.dbColumnToPythonAttr(k), v) for k, v in column_vals])
        dbvals['connection'] = self.transaction
        return (self.medium)(**dbvals)

    def visit_loader(self, loader):
        """Visit the loader and store a reference to the transaction connection"""
        self.transaction = loader.transaction


class SQLObjectFixture(DBLoadableFixture):
    __doc__ = '\n    A fixture that knows how to load DataSet objects via `SQLObject`_ classes.\n    \n    >>> from fixture import SQLObjectFixture\n    \n    Keyword Arguments:\n    \n    ``style``\n        A :class:`Style <fixture.style.Style>` object to translate names with\n    \n    ``env``\n        A dict or module that contains `SQLObject`_ classes.  The :class:`Style <fixture.style.Style>` object will \n        look here when translating DataSet names into `SQLObject`_ class names.\n        See :meth:`EnvLoadableFixture.attach_storage_medium <fixture.loadable.loadable.EnvLoadableFixture.attach_storage_medium>` for details on \n        how ``env`` works.\n    \n    ``dsn``\n        A dsn to create a connection with.\n    \n    ``dataclass``\n        :class:`SuperSet <fixture.dataset.SuperSet>` class to represent loaded data with\n    \n    ``medium``\n        A custom :class:`StorageMediumAdapter <fixture.loadable.loadable.StorageMediumAdapter>` to instantiate when storing a DataSet.\n    \n    ``use_transaction``\n        If this is true (default), data will be loaded or torn down inside a \n        transaction.  You may have to set this to false to avoid deadlocks.  \n        However, setting it to false may leave partially loaded data behind \n        if you create an error with your DataSet.\n    \n    ``close_conn``\n        True if the connection can be closed, helpful for releasing connections.  \n        If you are passing in a connection object this will be False by default.\n    \n    '

    def __init__(self, connection=None, use_transaction=True, close_conn=False, **kw):
        (DBLoadableFixture.__init__)(self, **kw)
        self.connection = connection
        self.close_conn = close_conn
        self.use_transaction = use_transaction

    SQLObjectMedium = SQLObjectMedium
    Medium = SQLObjectMedium

    def create_transaction(self):
        """Return a new transaction for connection"""
        from sqlobject import connectionForURI
        if not self.connection:
            self.connection = connectionForURI(self.dsn)
            self.close_conn = True
        if self.use_transaction:
            return self.connection.transaction()
        else:
            return self.connection

    def commit(self):
        """Commit transaction"""
        if self.use_transaction:
            DBLoadableFixture.commit(self)

    def then_finally(self, unloading=False):
        """Unconditionally close the transaction (if configured to do so) after loading data"""
        if unloading:
            if self.close_conn:
                self.connection.close()
                self.connection = None

    def rollback(self):
        """Rollback the transaction"""
        if self.use_transaction:
            DBLoadableFixture.rollback(self)