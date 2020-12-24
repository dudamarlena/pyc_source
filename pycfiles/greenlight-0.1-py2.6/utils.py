# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/greenlight/utils.py
# Compiled at: 2010-10-17 14:50:13
import sys
from functools import wraps

class DevNull(object):

    @staticmethod
    def write(m):
        pass


def hide_stderr(greenlet):
    """
    Patch a greenlet so it sends its extra error reporting to nowhere.
    """
    f = greenlet._report_error

    @wraps(f)
    def inner(self, *args, **kwargs):
        old_stderr = sys.stderr
        sys.stderr = DevNull
        try:
            return f(self, *args, **kwargs)
        finally:
            sys.stderr = old_stderr

    greenlet._report_error = inner