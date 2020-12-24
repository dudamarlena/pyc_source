# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/reporting/common.py
# Compiled at: 2009-10-07 18:08:46
"""Common functionality for reporting"""

def exc_info_to_string(err, test):
    """Converts a sys.exc_info()-style tuple of values into a string."""
    import traceback
    (exctype, value, tb) = err
    while tb and is_framework_traceback(tb):
        tb = tb.tb_next

    if exctype is test.failure_exception_type():
        length = count_framework_traceback_levels(tb)
        return ('').join(traceback.format_exception(exctype, value, tb, length))
    return ('').join(traceback.format_exception(exctype, value, tb))


def is_framework_traceback(tb):
    globals = tb.tb_frame.f_globals
    return globals.has_key('__unittest') or globals.has_key('__testoob')


def count_framework_traceback_levels(tb):
    length = 0
    while tb and not is_framework_traceback(tb):
        length += 1
        tb = tb.tb_next

    return length