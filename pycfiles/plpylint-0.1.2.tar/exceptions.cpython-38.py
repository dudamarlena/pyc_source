# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ben/Code/plpygis/plpygis/exceptions.py
# Compiled at: 2018-01-22 18:57:41
# Size of source mod 2**32: 1233 bytes


class PlpygisError(Exception):
    """PlpygisError"""

    def __init__(self, msg):
        super(PlpygisError, self).__init__(msg)


class DependencyError(PlpygisError, ImportError):
    """DependencyError"""

    def __init__(self, dep, msg=None):
        if msg is None:
            msg = "Dependency '{}' is not available.".format(dep)
        super(DependencyError, self).__init__(msg)


class WkbError(PlpygisError):
    """WkbError"""

    def __init__(self, msg=None):
        if msg is None:
            msg = 'Unreadable WKB.'
        super(WkbError, self).__init__(msg)


class DimensionalityError(PlpygisError):
    """DimensionalityError"""

    def __init__(self, msg=None):
        if msg is None:
            msg = 'Geometry has invalid dimensionality.'
        super(DimensionalityError, self).__init__(msg)


class SridError(PlpygisError):
    """SridError"""

    def __init__(self, msg=None):
        if msg is None:
            msg = 'Geometry has invalid SRID.'
        super(SridError, self).__init__(msg)