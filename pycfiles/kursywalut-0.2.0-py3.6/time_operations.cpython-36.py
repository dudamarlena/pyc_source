# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kursywalut/funcs/time_operations.py
# Compiled at: 2018-12-20 11:59:26
# Size of source mod 2**32: 727 bytes
"""Time Operations Package."""
from datetime import datetime
__author__ = 'Bart Grzybicki'

def now(return_type=None):
    """Return current time.

    Args:
        return_type (type): Optional argument, pass str() if you want
            to get string.

    Returns:
        date in datetime format or as a string.

    """
    if return_type == str():
        return str(datetime.now())
    else:
        return datetime.now()


def elapsed_time(time_start, time_end):
    """Return time difference.

    Args:
        time_start (datetime): start time.
        time_end (datetime): end time.

    Returns:
        datetime: difference between two times.

    """
    return time_end - time_start