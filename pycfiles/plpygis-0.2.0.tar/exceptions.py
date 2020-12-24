# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: plpygis/exceptions.py
# Compiled at: 2018-01-22 18:57:41


class PlpygisError(Exception):
    """
    Basic exception for ``plpygis``.
    """

    def __init__(self, msg):
        super(PlpygisError, self).__init__(msg)


class DependencyError(PlpygisError, ImportError):
    """
    Exception for a missing dependency.
    """

    def __init__(self, dep, msg=None):
        if msg is None:
            msg = ("Dependency '{}' is not available.").format(dep)
        super(DependencyError, self).__init__(msg)
        return


class WkbError(PlpygisError):
    """
    Exception for problems in parsing WKBs.
    """

    def __init__(self, msg=None):
        if msg is None:
            msg = 'Unreadable WKB.'
        super(WkbError, self).__init__(msg)
        return


class DimensionalityError(PlpygisError):
    """
    Exception for problems in dimensionality of geometries.
    """

    def __init__(self, msg=None):
        if msg is None:
            msg = 'Geometry has invalid dimensionality.'
        super(DimensionalityError, self).__init__(msg)
        return


class SridError(PlpygisError):
    """
    Exception for problems in dimensionality of geometries.
    """

    def __init__(self, msg=None):
        if msg is None:
            msg = 'Geometry has invalid SRID.'
        super(SridError, self).__init__(msg)
        return