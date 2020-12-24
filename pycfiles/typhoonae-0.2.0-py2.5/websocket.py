# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/typhoonae/websocket/websocket.py
# Compiled at: 2010-12-12 04:36:57
"""This module contains TyphoonAE's WebSocket API.

This module allows App Engine apps to interact with Web Sockets held by a
decoupled Web Socket Service.
"""
from google.appengine.api import apiproxy_stub_map
from google.appengine.runtime import apiproxy_errors
from typhoonae.websocket import websocket_service_pb2
__all__ = [
 'WEBSOCKET_HEADER',
 'WEBSOCKET_HANDLER_URL',
 'BadArgumentError',
 'create_websocket_url',
 'Message',
 'send_message',
 'broadcast_message']
WEBSOCKET_HEADER = 'X-TyphoonAE-WebSocket'
WEBSOCKET_HANDLER_URL = '%(protocol)s://%(host)s:%(port)s/%(app_key)s/%(success_path)s'

class Error(Exception):
    """Base error class for this module."""
    pass


class BadArgumentError(Error):
    """Raised when a method gets a bad argument."""
    pass


def create_websocket_url(success_path='', _make_sync_call=apiproxy_stub_map.MakeSyncCall):
    """Create a valid Web Socket URL.

    Args:
        success_path: Path within application to call when a new Web Socket
            request received.
        _make_sync_call: Used for dependency injection.

    Returns:
        String containing a valid Web Socket URL.
    """
    request = websocket_service_pb2.CreateWebSocketURLRequest()
    response = websocket_service_pb2.CreateWebSocketURLResponse()
    request.success_path = success_path
    _make_sync_call('websocket', 'CreateWebSocketURL', request, response)
    return response.url


class Message(object):
    """Class to represent a Web Socket message."""

    def __init__(self, vars):
        """Constructor.

        Args:
            vars: A dict-like object to extract message arguments from.
        """
        self.__body = vars['body']
        self.__socket = vars['from']

    @property
    def body(self):
        return self.__body

    @property
    def socket(self):
        return self.__socket


def send_message(sockets, body, _make_sync_call=apiproxy_stub_map.MakeSyncCall):
    """Sends a message to the Web Socket.

    Args:
        sockets: A list of connected Web Sockets.
        body: The message body.
        _make_sync_call: Used for dependency injection.
    """
    if isinstance(sockets, basestring):
        sockets = [
         sockets]
    if not isinstance(sockets, list):
        raise BadArgumentError('first argument of the send_message method must be a list.')
    for sock in sockets:
        if not sock:
            raise BadArgumentError('must specify sockets.')
        request = websocket_service_pb2.WebSocketMessageRequest()
        response = websocket_service_pb2.WebSocketMessageResponse()
        request.message.body = body
        request.message.socket = sock
        try:
            _make_sync_call('websocket', 'SendMessage', request, response)
        except apiproxy_errors.ApplicationError, e:
            raise Error()


def broadcast_message(body, _make_sync_call=apiproxy_stub_map.MakeSyncCall):
    """Sends a message to all active Web Sockets.

    Args:
        body: The message body.
        _make_sync_call: Used for dependency injection.
    """
    request = websocket_service_pb2.WebSocketMessageRequest()
    response = websocket_service_pb2.WebSocketMessageResponse()
    request.message.body = body
    try:
        _make_sync_call('websocket', 'BroadcastMessage', request, response)
    except apiproxy_errors.ApplicationError, e:
        raise Error()