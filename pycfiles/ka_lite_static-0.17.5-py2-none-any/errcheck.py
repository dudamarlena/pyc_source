# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/gis/geos/prototypes/errcheck.py
# Compiled at: 2018-07-11 18:15:30
"""
 Error checking functions for GEOS ctypes prototype functions.
"""
import os
from ctypes import c_void_p, string_at, CDLL
from django.contrib.gis.geos.error import GEOSException
from django.contrib.gis.geos.libgeos import GEOS_VERSION
from django.contrib.gis.geos.prototypes.threadsafe import GEOSFunc
if GEOS_VERSION >= (3, 1, 1):
    free = GEOSFunc('GEOSFree')
    free.argtypes = [c_void_p]
    free.restype = None
else:
    if os.name == 'nt':
        libc = CDLL('msvcrt')
    else:
        libc = CDLL(None)
    free = libc.free

def last_arg_byref(args):
    """Returns the last C argument's value by reference."""
    return args[(-1)]._obj.value


def check_dbl(result, func, cargs):
    """Checks the status code and returns the double value passed in by reference."""
    if result != 1:
        return None
    else:
        return last_arg_byref(cargs)


def check_geom(result, func, cargs):
    """Error checking on routines that return Geometries."""
    if not result:
        raise GEOSException('Error encountered checking Geometry returned from GEOS C function "%s".' % func.__name__)
    return result


def check_minus_one(result, func, cargs):
    """Error checking on routines that should not return -1."""
    if result == -1:
        raise GEOSException('Error encountered in GEOS C function "%s".' % func.__name__)
    else:
        return result


def check_predicate(result, func, cargs):
    """Error checking for unary/binary predicate functions."""
    val = ord(result)
    if val == 1:
        return True
    if val == 0:
        return False
    raise GEOSException('Error encountered on GEOS C predicate function "%s".' % func.__name__)


def check_sized_string(result, func, cargs):
    """
    Error checking for routines that return explicitly sized strings.

    This frees the memory allocated by GEOS at the result pointer.
    """
    if not result:
        raise GEOSException('Invalid string pointer returned by GEOS C function "%s"' % func.__name__)
    s = string_at(result, last_arg_byref(cargs))
    free(result)
    return s


def check_string(result, func, cargs):
    """
    Error checking for routines that return strings.

    This frees the memory allocated by GEOS at the result pointer.
    """
    if not result:
        raise GEOSException('Error encountered checking string return value in GEOS C function "%s".' % func.__name__)
    s = string_at(result)
    free(result)
    return s


def check_zero(result, func, cargs):
    """Error checking on routines that should not return 0."""
    if result == 0:
        raise GEOSException('Error encountered in GEOS C function "%s".' % func.__name__)
    else:
        return result