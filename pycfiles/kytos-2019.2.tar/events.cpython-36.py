# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/humberto/src/kytos/kytos-asyncio/kytos/core/events.py
# Compiled at: 2019-06-06 13:59:39
# Size of source mod 2**32: 1933 bytes
"""Module with Kytos Events."""
from kytos.core.helpers import now

class KytosEvent:
    __doc__ = 'Base Event class.\n\n    The event data will be passed in the `content` attribute, which should be a\n    dictionary.\n    '

    def __init__(self, name=None, content=None):
        """Create an event to be published.

        Args:
            name (string): The name of the event. You should prepend it with
                           the name of the napp.
            content (dict): Dictionary with any extra data for the event.
        """
        self.name = name
        self.content = content if content is not None else {}
        self.timestamp = now()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"KytosEvent({self.name!r}, {self.content!r})"

    @property
    def destination(self):
        """Return the destination of KytosEvent."""
        return self.content.get('destination')

    def set_destination(self, destination):
        """Update the destination of KytosEvent.

        Args:
            destination (string): destination of KytosEvent.
        """
        self.content['destination'] = destination

    @property
    def source(self):
        """Return the source of KytosEvent."""
        return self.content.get('source')

    def set_source(self, source):
        """Update the source of KytosEvent.

        Args:
            source (string): source of KytosEvent.
        """
        self.content['source'] = source

    @property
    def message(self):
        """Return the message carried by the event if it exists.

        If there is any OpenFlow message on the event it'll be stored on
        the 'message' key of the 'content' attribute.

        Returns:
            A python-openflow message instance if it exists, None otherwise.

        """
        try:
            return self.content['message']
        except KeyError:
            return