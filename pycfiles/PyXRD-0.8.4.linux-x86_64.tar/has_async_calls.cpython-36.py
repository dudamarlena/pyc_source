# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/generic/asynchronous/has_async_calls.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 1078 bytes
import logging
logger = logging.getLogger(__name__)
from .providers import get_provider
from .exceptions import *
from .dummy_async_server import DummyAsyncServer

class HasAsyncCalls(object):
    __doc__ = '\n        Class providing utility functions for async calls\n    '

    def submit_async_call(self, func):
        """ Utility that passes function calls down to the async server """
        try:
            self._async_server = get_provider().get_server()
        except (ServerNotRunningException, ServerStartTimeoutExcecption):
            logger.warning('Could not get the default provided async server, using dummy implementation')
            self._async_server = DummyAsyncServer()

        return self._async_server.submit(func)

    def fetch_async_result(self, result):
        """ Utility that parses the result objects returned by submit_async_call"""
        return result.get()