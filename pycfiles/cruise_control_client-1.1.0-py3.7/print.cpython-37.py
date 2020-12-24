# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/cruisecontrolclient/util/print.py
# Compiled at: 2019-06-19 12:58:27
# Size of source mod 2**32: 509 bytes
import sys

def print_error(*args, sep=' ', end='\n'):
    """
    Like the print() builtin, but presumes printing to stderr, rather than stdout
    :param sep:   string inserted between values, default a space.
    :param end:   string appended after the last value, default a newline.
    :return:
    """
    print(*args, sep=sep, end=end, file=sys.stderr)