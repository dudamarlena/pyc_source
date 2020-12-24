# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opendxl/viji/opendxl-console/dxlconsole/handlers.py
# Compiled at: 2019-06-07 18:26:01
from __future__ import absolute_import
from tornado.web import RequestHandler

class BaseRequestHandler(RequestHandler):
    """
    The base class for Tornado request handlers
    """

    def get_current_user(self):
        """
        Returns the current user for the request

        :return: The current user for the request
        """
        return self.get_secure_cookie(self.application.bootstrap_app.user_cookie_name)

    def data_received(self, chunk):
        """Implement this method to handle streamed request data.

        Requires the `.stream_request_body` decorator.
        """
        raise NotImplementedError()


class WebSocketEventHandler(object):
    """
    The base class for handling web socket events
    """

    def __init__(self):
        pass

    def on_web_socket_opened(self, client_id, web_socket):
        """
        Invoked whenever a new web socket is opened

        :param client_id: the client owning the web socket
        :param web_socket: the newly opened web socket
        """
        pass

    def on_web_socket_closed(self, client_id, web_socket):
        """
        Invoked whenever a web socket is closed

        :param client_id: the client owning the web socket
        :param web_socket:  the web socket being closed
        """
        pass

    def on_web_socket_message(self, client_id, message):
        """
        Invoked when a new message is received from a web socket

        :param client_id: the client owning the web socket
        :param message: the message received
        """
        pass