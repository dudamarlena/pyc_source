# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ghetzel/src/github.com/PerformLine/python-performline-client/build/lib.linux-x86_64-2.7/performline/embedded/stdlib/utils/types.py
# Compiled at: 2018-05-17 16:01:23
"""
Python type system extensions and utilities.
"""
import six, collections
PRIMITIVE_TYPES = (
 bool, int, float, complex, str, list, tuple, dict)
if six.PY2:
    PRIMITIVE_TYPES += (long, unicode)

def isprimitive(value):
    """
    Returns whether a given value is a primitive type or not.

    Args:
        value (any): The value to test.

    Returns:
        bool
    """
    if value is None or isinstance(value, PRIMITIVE_TYPES):
        return True
    return False


def isiterable(value):
    if isinstance(value, collections.Iterable):
        if not isinstance(value, basestring):
            return True
    return False


def iskindofexception(exc, match_values, check_in_message=True):
    if not isinstance(exc, Exception):
        raise ValueError('Must provide an Exception')
    if not isinstance(match_values, list):
        match_values = [
         match_values]
    if exc.__class__.__name__ in match_values:
        return True
    if check_in_message:
        for name in match_values:
            if name in exc.message:
                return True

    return False