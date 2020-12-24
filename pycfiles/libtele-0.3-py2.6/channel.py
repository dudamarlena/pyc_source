# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tele/channel.py
# Compiled at: 2011-01-14 09:58:16
from __future__ import unicode_literals

class Channel(object):
    """
    Represents a single TV-channel.
    """

    def __init__(self, key, name):
        self.key = key
        self.name = name

    def __eq__(self, other):
        return self.key == other.key and self.name == other.name

    def __ne__(self, other):
        return not self == other


class ChannelList(list):
    """
    This extends ``list`` with some utilitiy methods to find channels.
    """

    def get_by_name(self, name):
        """
        Returns the first channel in the list that has the given name. Raises
        an ``KeyError`` if the given name is not found.
        """
        for channel in self:
            if channel.name == name:
                return channel

        raise KeyError

    def get_by_key(self, key):
        """
        Returns the first channel in the list that has the given key. Raises
        an ``KeyError`` if the given name is not found.
        """
        for channel in self:
            if channel.key == key:
                return channel

        raise KeyError