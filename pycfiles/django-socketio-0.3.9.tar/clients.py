# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/steve/dev/django-socketio/django_socketio/clients.py
# Compiled at: 2013-11-04 16:45:11
from django_socketio import events
CLIENTS = {}

def client_start(request, socket, context):
    """
    Adds the client triple to CLIENTS.
    """
    CLIENTS[socket.session.session_id] = (
     request, socket, context)


def client_end(request, socket, context):
    """
    Handles cleanup when a session ends for the given client triple.
    Sends unsubscribe and finish events, actually unsubscribes from
    any channels subscribed to, and removes the client triple from
    CLIENTS.
    """
    for channel in socket.channels:
        events.on_unsubscribe.send(request, socket, context, channel)

    events.on_finish.send(request, socket, context)
    for channel in socket.channels[:]:
        socket.unsubscribe(channel)

    del CLIENTS[socket.session.session_id]


def client_end_all():
    """
    Performs cleanup on all clients - called by runserver_socketio
    when the server is shut down or reloaded.
    """
    for request, socket, context in CLIENTS.values()[:]:
        client_end(request, socket, context)