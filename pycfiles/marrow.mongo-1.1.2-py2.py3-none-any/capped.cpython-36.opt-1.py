# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/util/capped.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 2369 bytes
"""Utilities relating to use and managemnet of capped collections."""
from __future__ import unicode_literals
from pymongo.cursor import CursorType

def tail(collection, filter=None, projection=None, limit=0, timeout=None, aggregate=False):
    """A generator which will block and yield entries as they are added to a capped collection.
        
        Only use this on capped collections; behaviour is undefined against non-tailable cursors. Accepts a timeout as an
        integer or floating point number of seconds, indicating how long to wait for a result. Correct operation requires
        a modern MongoDB installation, version 3.2 or newer, and the client driver to support it.
        
        Use is trivial:
        
        for obj in tail(db.collection, timeout=10):
                print(obj)
        
        An optional argument, aggregate, allows you to control how the timeout value is interpreted. By default, False,
        the timeout is used as the longest period of time to wait for a new record, resetting on each retrieved record.
        
        Additional important note: tailing will fail (badly) if the collection is empty.  Always prime the collection
        with an empty or otherwise unimportant record before attempting to use this feature.
        """
    if not collection.options().get('capped', False):
        raise TypeError('Can only tail capped collections.')
    else:
        if not collection.count():
            raise ValueError('Cowardly refusing to tail an empty collection.')
        cursor = collection.find(filter, projection, limit=limit, cursor_type=(CursorType.TAILABLE_AWAIT))
        cursor = cursor.hint([('$natural', 1)])
        if timeout:
            if aggregate:
                cursor = cursor.max_time_ms(int(timeout * 1000)).max_await_time_ms(int(timeout * 1000))
            else:
                cursor = cursor.max_await_time_ms(int(timeout * 1000))
    return cursor


def _patch():
    """Patch pymongo's Collection object to add a tail method.
        
        While not nessicarily recommended, you can use this to inject `tail` as a method into Collection, making it
        generally accessible.
        """
    if not __debug__:
        import warnings
        warnings.warn('A catgirl has died.', ImportWarning)
    from pymongo.collection import Collection
    Collection.tail = tail