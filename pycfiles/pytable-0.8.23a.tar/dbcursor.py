# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mcfletch/pylive/table/pytable/dbcursor.py
# Compiled at: 2003-09-14 17:25:13
"""Cursor object which retains link to connection object"""
from __future__ import generators
from basicproperty import propertied, basic
_formatMap = {'named': (0, ':%(name)s'), 
   'pyformat': (0, '%%(%(name)s)s'), 
   'qmark': (1, '?'), 
   'numeric': (1, ':%(position)s'), 
   'format': (1, '%%s')}

class DBCursor(propertied.Propertied):
    """DBConnection-aware cursor-object wrapper

        The DBCursor object provides a few extended DB-API
        features, particularly retaining a link to the connection
        which created the cursor, and providing for iteration
        across a cursor's result set.

        Cursor Attributes .connection

                This read-only attribute return a reference to the Connection
                object on which the cursor was created.

                The attribute simplifies writing polymorphic code in
                multi-connection environments.

        Cursor Method .__iter__()
        """
    cursor = basic.BasicProperty('cursor', 'Pointer to the underlying DB-API cursor object')
    connection = basic.BasicProperty('connection', 'Pointer to the DBConnection instance which created the cursor\n\n\t\tThis implements the .connection DB-API extension\n\t\t')

    def __getattr__(self, key):
        """Defer to the connection for attribute lookup"""
        if key != 'cursor':
            try:
                return getattr(self.cursor, key)
            except AttributeError:
                pass

        raise AttributeError('%s instance has no attribute %s' % (self.__class__.__name__, key))

    def parameterFormat(self, name, position=0):
        """Format paramname for the driver

                returns (positional (boolean), formattedName)

                XXX Note: this isn't AFAIK actually used anywhere, so
                        it could quite easily be dropped.
                """
        formatName = self.connection.driver.paramstyle
        (positional, format) = _formatMap.get(formatName)
        return (positional, format % locals())

    def __iter__(self):
        """Create an iterator for the cursor

                This method creates a generator which yields
                self.fetchone() until fetchone returns None
                (or fails).  If fetchone fails the exception
                is ignored and the iterator terminates.
                """
        try:
            item = self.fetchone()
        except Exception:
            item = None

        while item:
            yield item
            try:
                item = self.fetchone()
            except Exception:
                item = None

        return