# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/generic/asynchronous/dummy_async_result.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 344 bytes


class DummyAsyncResult(object):
    __doc__ = ' A non-asynchronous dummy implementation of the AsyncResult object '

    def __init__(self, func):
        self.result = func()

    def get(self):
        return self.result