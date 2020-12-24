# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/generic/asynchronous/dummy_async_server.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 439 bytes
from .dummy_async_result import DummyAsyncResult

class DummyAsyncServer(object):
    __doc__ = ' A non-asynchronous dummy implementation of the AsyncServer object '

    def loopCondition(self):
        return True

    def submit(self, func):
        return DummyAsyncResult(func)

    def shutdown(self):
        pass