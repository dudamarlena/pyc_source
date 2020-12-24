# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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