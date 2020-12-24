# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \.\cx_Freeze\common.py
# Compiled at: 2019-08-29 22:24:38
# Size of source mod 2**32: 446 bytes
__doc__ = '\nThis module contains utility functions shared between cx_Freeze modules.\n'

def normalize_to_list(value):
    """
    Takes the different formats of options containing multiple values and
    returns the value as a list object.
    """
    if value is None:
        normalizedValue = []
    else:
        if isinstance(value, str):
            normalizedValue = value.split(',')
        else:
            normalizedValue = list(value)
    return normalizedValue