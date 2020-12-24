# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/devproxy/handlers/wurfl_handler/simple.py
# Compiled at: 2014-07-28 10:42:31
from devproxy.handlers.wurfl_handler.base import WurflHandler

class SimpleWurflHandler(WurflHandler):

    def handle_device(self, request, device):
        if device.resolution_width <= 240:
            return [{self.header_name: 'medium'}]
        else:
            return [{self.header_name: 'high'}]


class SimpleWurflTestHandler(SimpleWurflHandler):
    """Handler used in tests. Do not use in production."""

    def handle_user_agent(self, user_agent):
        if user_agent == 'Some special bot':
            return [{self.header_name: 'bot'}]
        else:
            return