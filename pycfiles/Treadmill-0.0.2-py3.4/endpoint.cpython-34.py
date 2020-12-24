# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/websocket/api/endpoint.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 1542 bytes
"""
A WebSocket handler for Treadmill state.
"""
import os, logging
_LOGGER = logging.getLogger(__name__)

class EndpointAPI(object):
    __doc__ = 'Handler for /endpoints topic.'

    def subscribe(self, message):
        """Return filter based on message payload."""
        app_filter = message['filter']
        proto = message.get('proto')
        if not proto:
            proto = '*'
        endpoint = message.get('endpoint')
        if not endpoint:
            endpoint = '*'
        proid, pattern = app_filter.split('.', 1)
        if '#' not in pattern:
            pattern += '#*'
        full_pattern = ':'.join([pattern, proto, endpoint])
        return [(os.path.join('/endpoints', proid), full_pattern)]

    def on_event(self, filename, operation, content):
        """Event handler."""
        if operation == 'c':
            return
        if not filename.startswith('/endpoints/'):
            return
        proid, endpoint_file = filename[len('/endpoints/'):].split('/', 1)
        host = None
        port = None
        if content is not None:
            host, port = content.split(':')
        sow = operation is None
        app, proto, endpoint = endpoint_file.split(':')
        return {'topic': '/endpoints', 
         'name': '.'.join([proid, app]), 
         'proto': proto, 
         'endpoint': endpoint, 
         'host': host, 
         'port': port, 
         'sow': sow}


def init():
    """API module init."""
    return [
     (
      '/endpoints', EndpointAPI())]