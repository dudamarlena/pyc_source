# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/schevo/constant.py
# Compiled at: 2007-03-21 14:34:41
"""Schevo primitive types and constants.

For copyright, license, and warranty, see bottom of file.
"""
import sys
from schevo.lib import optimize

class _GLOBAL(type):
    """Base metaclass for global values."""
    __module__ = __name__

    def __repr__(cls):
        return cls.__name__

    def __str__(cls):
        return '<%s>' % (cls.__name__,)


class _FALSE(_GLOBAL):
    """Base metaclass for global, false field values."""
    __module__ = __name__

    def __nonzero__(cls):
        return False


class _UNASSIGNED(_FALSE):
    """Base metaclass for UNASSIGNED."""
    __module__ = __name__

    def __cmp__(cls, other):
        if other is UNASSIGNED:
            return 0
        else:
            return -1

    def __str__(cls):
        return ''


class ANY(object):
    """Any entity type is allowed."""
    __module__ = __name__
    __metaclass__ = _GLOBAL


class CASCADE(object):
    """Cascade delete on entity field."""
    __module__ = __name__
    __metaclass__ = _GLOBAL


class DEFAULT(object):
    """Use the default field value when specifying sample or initial
    data to populate database."""
    __module__ = __name__
    __metaclass__ = _GLOBAL


class RESTRICT(object):
    """Restrict delete on entity field."""
    __module__ = __name__
    __metaclass__ = _GLOBAL


class UNASSIGN(object):
    """Unassign delete on entity field."""
    __module__ = __name__
    __metaclass__ = _GLOBAL


class UNASSIGNED(object):
    """Field value or field default value is unassigned."""
    __module__ = __name__
    __metaclass__ = _UNASSIGNED
    _label = '<UNASSIGNED>'

    def __init__(self):
        raise TypeError('%r object is not callable' % self.__class__.__name__)


optimize.bind_all(sys.modules[__name__])