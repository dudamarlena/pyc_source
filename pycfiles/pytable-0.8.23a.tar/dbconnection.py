# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mcfletch/pylive/table/pytable/dbconnection.py
# Compiled at: 2004-02-19 05:40:14
"""Wrapper for connection objects which retain access to driver"""
from basicproperty import propertied, basic, common

class DBConnection(propertied.Propertied):
    """DB-driver-aware connection-object wrapper

        The primary purpose of the wrapper here is to retain
        a link to the driver object which created the connection.
        The connection otherwise defers to the underlying
        DB-API connection object.

        The secondary purpose of the connection is to override
        the cursor method to return a dbcursor.DBCursor instance
        rather than a raw DB-API cursor object.  You can customize
        the class of the cursor object by setting the
        defaultCursorClass property of the connection.
        """
    specifier = basic.BasicProperty('specifier', 'Pointer to the specifier used to connect')
    connection = basic.BasicProperty('connection', 'Pointer to the underlying DB-API connection')
    driver = basic.BasicProperty('driver', 'Pointer to the DBDriver instance which created this connection')
    invalid = common.BooleanProperty('invalid', 'The connection has become invalid, normally as a result of an OperationalError, reconnect!', defaultValue=0)
    defaultCursorClass = common.ClassByNameProperty('defaultCursorClass', "DBCursor sub-class to be used for this connection\n\n\t\tThe class' constructor should have a signature similar to\n\t\t\n\t\t\tclassObject( cursor = <cursor>, connection = <conn> )\n\t\t\t\n\t\twhich will be called with named arguments.\n\t\t", defaultValue='pytable.dbcursor.DBCursor')

    def reconnect(self):
        """Reconnect an invalid connection using it's specifier"""
        (self.driver, self.connection) = self.specifier.connect()
        self.invalid = 0
        return self

    def cursor(self):
        """Open and return a new DBCursor instance for this connection

                Normally the returned cursor will be an instance of the
                pytable.dbcursor.DBCursor class, this can be overridden
                by setting the defaultCursorClass property of the
                connection.
                """
        return self.defaultCursorClass(cursor=self.connection.cursor(), connection=self)

    def rollback(self):
        """Mark ourselves invalid and pass call to our base connection"""
        try:
            return self.connection.rollback()
        finally:
            self.invalid = 1

    def __getattr__(self, key):
        """Defer to the connection for attribute lookup"""
        if key != 'connection':
            try:
                return getattr(self.connection, key)
            except AttributeError:
                pass

        raise AttributeError('%s instance has no attribute %r' % (self.__class__.__name__, key))