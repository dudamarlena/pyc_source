# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/app/tcrudge/utils/validation.py
# Compiled at: 2016-12-08 09:48:39
# Size of source mod 2**32: 1068 bytes
"""
Module for common validation tools.
"""

def validate_integer(val, min_value=None, max_value=None, default=None):
    """
    Validates the input val parameter.

    If it is can not be converted to integer, returns default_value.

    If it is less than min_value, returns min_value.

    If it is greater than max_value, returns max_value.

    :param val: number to validate
    :type val: int, float, digital string

    :param min_value: min value of validation range
    :type min_value: int

    :param max_value: max value of validation range
    :type max_value: int

    :param default: default value to return in case of exception
    :type default: int

    :return: None, min, max, default or result - int
    :rtype: NoneType, int
    """
    try:
        result = int(val)
    except (TypeError, ValueError):
        return default

    if min_value is not None and result < min_value:
        result = min_value
    if max_value is not None and result > max_value:
        result = max_value
    return result