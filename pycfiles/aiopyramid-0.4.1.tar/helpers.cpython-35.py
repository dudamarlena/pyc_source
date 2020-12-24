# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/housl/workspaces/develop/aiopyramid/aiopyramid/websocket/helpers.py
# Compiled at: 2015-11-19 15:43:13
# Size of source mod 2**32: 405 bytes
from .exceptions import WebsocketClosed

def ignore_websocket_closed(app):
    """ Wrapper for ignoring closed websockets. """

    def _call_app_ignoring_ws_closed(environ, start_response):
        try:
            return app(environ, start_response)
        except WebsocketClosed as e:
            if e.__cause__:
                raise
            return ''

    return _call_app_ignoring_ws_closed