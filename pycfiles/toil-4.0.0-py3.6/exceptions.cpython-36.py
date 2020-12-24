# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/lib/exceptions.py
# Compiled at: 2020-04-03 17:41:24
# Size of source mod 2**32: 2107 bytes
from __future__ import absolute_import
from future.utils import raise_
from builtins import object
import sys

class panic(object):
    __doc__ = '\n    The Python idiom for reraising a primary exception fails when the except block raises a\n    secondary exception, e.g. while trying to cleanup. In that case the original exception is\n    lost and the secondary exception is reraised. The solution seems to be to save the primary\n    exception info as returned from sys.exc_info() and then reraise that.\n\n    This is a contextmanager that should be used like this\n\n    try:\n         # do something that can fail\n    except:\n        with panic( log ):\n            # do cleanup that can also fail\n\n    If a logging logger is passed to panic(), any secondary Exception raised within the with\n    block will be logged. Otherwise those exceptions are swallowed. At the end of the with block\n    the primary exception will be reraised.\n    '

    def __init__(self, log=None):
        super(panic, self).__init__()
        self.log = log
        self.exc_info = None

    def __enter__(self):
        self.exc_info = sys.exc_info()

    def __exit__(self, *exc_info):
        if self.log is not None:
            if exc_info:
                if exc_info[0]:
                    self.log.warning('Exception during panic', exc_info=exc_info)
        exc_type, exc_value, traceback = self.exc_info
        raise_(exc_type, exc_value, traceback)