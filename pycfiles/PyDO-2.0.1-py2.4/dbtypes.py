# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydo/dbtypes.py
# Compiled at: 2007-02-15 13:23:36
"""

The dbtypes module contains generic type wrapper classes for values
passed into PyDO, to provide type information useful into marshalling
the data into SQL according to the intended datatype.  Some mapping of
datatype can be done solely on the basis of Python type, but at times
it may be necessary to be more specific.

DBAPI-compliant drivers use wrapper classes for this purpose, but they
are specific to the underlying driver; these wrappers can be used
with all drivers.

If you insert or update a wrapped value into a PyDO instance, the
value of the corresponding column in that instance will be the
unwrapped value, not the wrapper itself.

"""

class typewrapper(object):
    __module__ = __name__
    __slots__ = ('value', )

    def __init__(self, value):
        self.value = value


class DATE(typewrapper):
    __module__ = __name__


class TIMESTAMP(typewrapper):
    __module__ = __name__


class INTERVAL(typewrapper):
    __module__ = __name__


class BINARY(typewrapper):
    __module__ = __name__


def unwrap(val):
    if isinstance(val, typewrapper):
        return val.value
    return val


date_formats = [
 '%m-%d-%Y', '%m-%d-%y', '%Y-%d-%m', '%y-%d-%m', '%B %d %Y', '%b %d %Y', '%d %B %Y', '%d %b %Y']
timestamp_formats = [
 '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%y-%m-%d %H:%M:%S']
__all__ = [
 'DATE', 'TIMESTAMP', 'INTERVAL', 'BINARY']