# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solo/apps/hello/handlers.py
# Compiled at: 2016-03-29 19:17:50
# Size of source mod 2**32: 268 bytes
from solo import http_endpoint, http_defaults

@http_defaults(route_name='solo.hello')
class HelloWorld:

    def __init__(self, request):
        self.request = request

    @http_endpoint(request_method='GET')
    async def get(self):
        return 'Hello World!'