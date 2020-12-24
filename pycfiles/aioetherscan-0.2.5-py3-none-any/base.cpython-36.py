# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aioetcd3/base.py
# Compiled at: 2018-05-26 21:48:07
# Size of source mod 2**32: 789 bytes
_default_timeout = object()

class StubMixin(object):

    def __init__(self, channel, timeout):
        self.channel = channel
        self.timeout = timeout
        self.last_response_info = None
        self._update_channel(channel)

    def _update_channel(self, channel):
        self.channel = channel
        self._loop = channel._loop

    def _update_cluster_info(self, header):
        self.last_response_info = header

    def get_cluster_info(self):
        return self.last_response_info

    async def grpc_call(self, stub_func, request, timeout=_default_timeout):
        if timeout is _default_timeout:
            timeout = self.timeout
        response = await stub_func(request, timeout=timeout)
        self._update_cluster_info(response.header)
        return response