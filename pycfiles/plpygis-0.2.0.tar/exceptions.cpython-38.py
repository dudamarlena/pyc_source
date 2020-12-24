# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ben/Code/plpygis/plpygis/exceptions.py
# Compiled at: 2018-01-22 18:57:41
# Size of source mod 2**32: 1233 bytes


class PlpygisError(Exception):
    __doc__ = '\n    Basic exception for ``plpygis``.\n    '

    def __init__(self, msg):
        super(PlpygisError, self).__init__(msg)


class DependencyError(PlpygisError, ImportError):
    __doc__ = '\n    Exception for a missing dependency.\n    '

    def __init__(self, dep, msg=None):
        if msg is None:
            msg = "Dependency '{}' is not available.".format(dep)
        super(DependencyError, self).__init__(msg)


class WkbError(PlpygisError):
    __doc__ = '\n    Exception for problems in parsing WKBs.\n    '

    def __init__(self, msg=None):
        if msg is None:
            msg = 'Unreadable WKB.'
        super(WkbError, self).__init__(msg)


class DimensionalityError(PlpygisError):
    __doc__ = '\n    Exception for problems in dimensionality of geometries.\n    '

    def __init__(self, msg=None):
        if msg is None:
            msg = 'Geometry has invalid dimensionality.'
        super(DimensionalityError, self).__init__(msg)


class SridError(PlpygisError):
    __doc__ = '\n    Exception for problems in dimensionality of geometries.\n    '

    def __init__(self, msg=None):
        if msg is None:
            msg = 'Geometry has invalid SRID.'
        super(SridError, self).__init__(msg)