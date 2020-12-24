# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/nls/.virtualenvs/pysher/lib/python3.6/site-packages/pysher/channel.py
# Compiled at: 2020-03-30 13:48:15
# Size of source mod 2**32: 1412 bytes
from collections import defaultdict

class Channel(object):

    def __init__(self, channel_name, connection, auth=None):
        self.name = channel_name
        self.connection = connection
        self.event_callbacks = defaultdict(list)
        self.auth = auth

    def bind(self, event_name, callback, *args, **kwargs):
        """Bind an event to a callback

        :param event_name: The name of the event to bind to.
        :type event_name: str

        :param callback: The callback to notify of this event.
        """
        self.event_callbacks[event_name].append((callback, args, kwargs))

    def trigger(self, event_name, data):
        """Trigger an event on this channel.  Only available for private or
        presence channels

        :param event_name: The name of the event.  Must begin with 'client-''
        :type event_name: str

        :param data: The data to send with the event.
        """
        if self.connection:
            if event_name.startswith('client-'):
                if self.name.startswith('private-') or self.name.startswith('presence-'):
                    self.connection.send_event(event_name, data, channel_name=(self.name))

    def _handle_event(self, event_name, data):
        if event_name in self.event_callbacks.keys():
            for callback, args, kwargs in self.event_callbacks[event_name]:
                callback(data, *args, **kwargs)