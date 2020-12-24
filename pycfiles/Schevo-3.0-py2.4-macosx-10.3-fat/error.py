# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/schevo/store/error.py
# Compiled at: 2007-03-21 14:34:41
"""$URL: svn+ssh://svn.mems-exchange.org/repos/trunk/durus/error.py $
$Id: error.py 1475 2005-12-01 17:36:40Z mscott $
"""
from schevo.lib import optimize
from schevo.store.utils import format_oid

class DurusError(StandardError):
    """Durus error."""
    __module__ = __name__


class DurusKeyError(KeyError, DurusError):
    """Key not found in database."""
    __module__ = __name__

    def __str__(self):
        return format_oid(self.args[0])


class InvalidObjectReference(DurusError):
    """
    An object contains an invalid reference to another object.

    A reference is invalid if it refers to an object managed
    by a different database connection.

    Instance attributes:
      obj: Persistent
        is the object for which the reference is invalid.
      connection: Connection
        the connection that attempted to store it.
    
    obj._p_connection != connection
    """
    __module__ = __name__

    def __init__(self, obj, connection):
        self.obj = obj
        self.connection = connection

    def __str__(self):
        return 'Invalid reference to %r with a connection %r.' % (self.obj, self.obj._p_connection)


class ConflictError(DurusError):
    """
    Two transactions tried to modify the same object at once.
    This transaction should be resubmitted.
    The object passed to the constructor should be an instance of Persistent.
    """
    __module__ = __name__

    def __init__(self, oids):
        self.oids = oids

    def __str__(self):
        if len(self.oids) > 1:
            s = 'oids=[%s ...]'
        else:
            s = 'oids=[%s]'
        return s % format_oid(self.oids[0])


class ReadConflictError(ConflictError):
    """
    Conflict detected when object was loaded.
    An attempt was made to read an object that has changed in another
    transaction (eg. another process).
    """
    __module__ = __name__


class ProtocolError(DurusError):
    """
    An error occurred during communication between the storage server
    and the client.
    """
    __module__ = __name__


import sys
optimize.bind_all(sys.modules[__name__])