# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydo/dbtypes.py
# Compiled at: 2007-02-15 13:23:36
__doc__ = '\n\nThe dbtypes module contains generic type wrapper classes for values\npassed into PyDO, to provide type information useful into marshalling\nthe data into SQL according to the intended datatype.  Some mapping of\ndatatype can be done solely on the basis of Python type, but at times\nit may be necessary to be more specific.\n\nDBAPI-compliant drivers use wrapper classes for this purpose, but they\nare specific to the underlying driver; these wrappers can be used\nwith all drivers.\n\nIf you insert or update a wrapped value into a PyDO instance, the\nvalue of the corresponding column in that instance will be the\nunwrapped value, not the wrapper itself.\n\n'

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