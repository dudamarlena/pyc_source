# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kdb/plugins/broadcast.py
# Compiled at: 2014-04-26 09:00:59
"""Broadtcasting Support

This plugin provides support for listening to broadcast
messages by listening for a certain pattern of message
and performing some command or event on that.
"""
__version__ = '0.0.2'
__author__ = 'James Mills, prologic at shortcircuit dot net dot au'
from circuits import handler
from circuits.protocols.irc import message as MessageEvent
from ..plugin import BasePlugin

class Broadcast(BasePlugin):
    """Broadcasting Support"""

    def init(self, *args, **kwargs):
        super(Broadcast, self).init(*args, **kwargs)
        self.prefix = self.config.get('broadcast', {}).get('prefix', None) or '@'
        return

    @handler('message', priority=1.0)
    def _on_message(self, event, source, target, message):
        addressed, target, message = self.bot.is_addressed(source, target, message)
        if not addressed and len(message) > 0:
            if message[0] == self.prefix:
                self.fire(MessageEvent(source, target, ('{0:s}, {1:s}').format(self.data.state['nick'], message[1:])))
                event.stop()