# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kentcoble/Documents/workspace/easysnmp/easysnmp/utils.py
# Compiled at: 2016-04-23 17:04:30
from __future__ import unicode_literals
import string
from .compat import ub, text_type

def strip_non_printable(value):
    """
    Removes any non-printable characters and adds an indicator to the string
    when binary characters are fonud.

    :param value: the value that you wish to strip
    """
    if value is None:
        return
    else:
        printable_value = (b'').join(filter(lambda c: c in string.printable, value))
        if printable_value != value:
            if printable_value:
                printable_value += b' '
            printable_value += b'(contains binary)'
        return printable_value


def tostr(value):
    """
    Converts any variable to a string or returns None if the variable
    contained None to begin with; this function currently supports None,
    unicode strings, byte strings and numbers.

    :param value: the value you wish to convert to a string
    """
    if value is None:
        return
    else:
        if isinstance(value, text_type):
            return value
        else:
            if isinstance(value, (int, float)):
                return str(value)
            return ub(value)

        return