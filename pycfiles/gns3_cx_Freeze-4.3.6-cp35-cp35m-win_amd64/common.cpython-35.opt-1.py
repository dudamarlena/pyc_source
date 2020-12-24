# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \.\cx_Freeze\common.py
# Compiled at: 2016-04-18 03:12:47
# Size of source mod 2**32: 446 bytes
"""
This module contains utility functions shared between cx_Freeze modules.
"""

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