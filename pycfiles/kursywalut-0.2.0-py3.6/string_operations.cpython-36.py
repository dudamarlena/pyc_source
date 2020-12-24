# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kursywalut/funcs/string_operations.py
# Compiled at: 2018-12-20 11:59:26
# Size of source mod 2**32: 502 bytes
"""String Operations Package."""
import six
__author__ = 'Bart Grzybicki'

def _to_unicode(value):
    """Convert value to unicode.

    Args:
        value (str): Value to be converted to unicode.

    Returns:
        string (Python 3) or unicode (Python 2).

    """
    return six.text_type(value)


def print_unicode(string):
    """Print unicode function.

    Prints string (Python 3) or string converted to unicode (Python 2).

    """
    print(_to_unicode(string))