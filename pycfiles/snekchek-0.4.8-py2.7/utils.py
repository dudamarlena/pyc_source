# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snekchek/utils.py
# Compiled at: 2020-03-03 07:34:32
"""
This module provides redirect_* functions for Python <3.5
"""
import sys

class _RedirectStream(object):
    _stream = None

    def __init__(self, new_target):
        self._new_target = new_target
        self._old_targets = []

    def __enter__(self):
        self._old_targets.append(getattr(sys, self._stream))
        setattr(sys, self._stream, self._new_target)
        return self._new_target

    def __exit__(self, exctype, excinst, exctb):
        setattr(sys, self._stream, self._old_targets.pop())


class redirect_stdout(_RedirectStream):
    """Context manager for temporarily redirecting stdout to another file.
        # How to send help() to stderr
        with redirect_stdout(sys.stderr):
            help(dir)
        # How to write help() to a file
        with open('help.txt', 'w') as f:
            with redirect_stdout(f):
                help(pow)
    """
    _stream = 'stdout'


class redirect_stderr(_RedirectStream):
    """Context manager for temporarily redirecting stderr to another file."""
    _stream = 'stderr'