# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kdb/plugins/drone.py
# Compiled at: 2014-04-26 09:00:59
"""Drone Mode

This plugin enables drone-mode. For now this means
just setting the bot's nickname to the system hostname.
"""
__version__ = '0.0.3'
__author__ = 'James Mills, prologic at shortcircuit dot net dot au'
from socket import gethostname
from circuits import handler
from circuits.protocols.irc import NICK
from ..plugin import BasePlugin

class Drone(BasePlugin):
    """Drone Mode"""

    def init(self, *args, **kwargs):
        super(Drone, self).init(*args, **kwargs)
        if self.data.state['nick'] != gethostname():
            self.fire(NICK(gethostname()))

    @handler('connected', 'registered', 'nick')
    def update_nick(self, *args, **kwargs):
        if self.data.state['nick'] != gethostname():
            self.fire(NICK(gethostname()))