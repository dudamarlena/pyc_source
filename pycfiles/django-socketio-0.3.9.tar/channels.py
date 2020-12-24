# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/steve/dev/django-socketio/django_socketio/channels.py
# Compiled at: 2013-11-04 16:45:11
from collections import defaultdict
CHANNELS = defaultdict(list)

class SocketIOChannelProxy(object):
    """
    Proxy object for SocketIOProtocol that adds channel subscription
    and broadcast.
    """

    def __init__(self, socket):
        """
        Store the original socket protocol object.
        """
        self.socket = socket
        self.channels = []

    def subscribe(self, channel):
        """
        Add the channel to this socket's channels, and to the list of
        subscribed session IDs for the channel. Return False if
        already subscribed, otherwise True.
        """
        if channel in self.channels:
            return False
        CHANNELS[channel].append(self.socket.session.session_id)
        self.channels.append(channel)
        return True

    def unsubscribe(self, channel):
        """
        Remove the channel from this socket's channels, and from the
        list of subscribed session IDs for the channel. Return False
        if not subscribed, otherwise True.
        """
        try:
            CHANNELS[channel].remove(self.socket.session.session_id)
            self.channels.remove(channel)
        except ValueError:
            return False

        return True

    def broadcast_channel(self, message, channel=None):
        """
        Send the given message to all subscribers for the channel
        given. If no channel is given, send to the subscribers for
        all the channels that this socket is subscribed to.
        """
        if channel is None:
            channels = self.channels
        else:
            channels = [
             channel]
        for channel in channels:
            for subscriber in CHANNELS[channel]:
                if subscriber != self.socket.session.session_id:
                    session = self.socket.handler.server.sessions[subscriber]
                    self._write(message, session)

        return

    def send_and_broadcast(self, message):
        """
        Shortcut for a socket to broadcast to all sockets itself.
        """
        self.send(message)
        self.broadcast(message)

    def send_and_broadcast_channel(self, message, channel=None):
        """
        Shortcut for a socket to broadcast to all sockets subscribed
        to a channel, and itself.
        """
        self.send(message)
        self.broadcast_channel(message, channel)

    def __getattr__(self, name):
        """
        Proxy missing attributes to the socket.
        """
        return getattr(self.socket, name)