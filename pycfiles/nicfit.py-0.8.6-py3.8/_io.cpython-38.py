# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nicfit/console/_io.py
# Compiled at: 2017-09-13 00:01:00
# Size of source mod 2**32: 429 bytes
import sys

def pout(msg, log=None):
    """Print 'msg' to stdout, and option 'log' at info level."""
    _print(msg, (sys.stdout), log_func=(log.info if log else None))


def perr(msg, log=None):
    """Print 'msg' to stderr, and option 'log' at info level."""
    _print(msg, (sys.stderr), log_func=(log.error if log else None))


def _print(msg, file, log_func=None):
    print(msg, file=file)
    if log_func:
        log_func(msg)