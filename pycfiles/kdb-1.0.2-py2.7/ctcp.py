# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kdb/plugins/ctcp.py
# Compiled at: 2014-04-26 09:00:59
"""CTCP

This plugin provides responses to IRC CTCP Events and
responds to them appropiately.
"""
__version__ = '0.2'
__author__ = 'James Mills, prologic at shortcircuit dot net dot au'
from time import asctime
from circuits import handler
from circuits.protocols.irc import CTCPREPLY
import kdb
from ..plugin import BasePlugin

class CTCP(BasePlugin):
    """IRC CTCP Events Plugin

    This plugin provides responses to IRC CTCP Events and
    responds to them appropiately.

    NOTE: There are no commands for this plugin (yet).
    """

    @handler('ctcp')
    def _on_ctcp(self, source, target, type, message):
        """CTCP Event Handler

        Handle IRC CTCP Events and respond to them
        appropiately.
        """
        addressed, target, message = self.bot.is_addressed(source, target, message)
        if not addressed:
            return
        else:
            if type.lower() == 'ping':
                response = (
                 'PING', message)
            elif type.lower() == 'time':
                response = (
                 'TIME', asctime())
            elif type.lower() == 'version':
                response = ('VERSION',
                 ('{0:s} - v{1:s} ({2:s})').format(kdb.__name__, kdb.__version__, kdb.__url__))
            else:
                response = None
            if response is not None:
                self.fire(CTCPREPLY(target, *response))
            return