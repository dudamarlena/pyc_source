# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kdb/plugins/timers.py
# Compiled at: 2014-04-26 09:00:59
"""Timers

This plugin shows how to user the timers module.
Provides a test command to create a message to be
display in x seconds.
"""
__version__ = '0.0.2'
__author__ = 'James Mills, prologic at shortcircuit dot net dot au'
from circuits import Component, Timer
from circuits.protocols.irc import PRIVMSG
from funcy import first, second
from ..plugin import BasePlugin

class Commands(Component):
    channel = 'commands'

    def timer(self, source, target, args):
        """Create a new time with the given length and message

        Syntax: TIMER <duration> [<message>]
        """
        if not args:
            return 'No duration specified.'
        tokens = args.split(' ', 1)
        duration = first(tokens)
        message = second(tokens)
        try:
            duration = int(duration)
        except ValueError:
            return 'Invalid duration specified!'

        message = message or '{0:d}s timer expiered!'
        event = PRIVMSG(target, message)
        Timer(duration, event, channel='bot').register(self)
        return ('Timer set for {0:d}s').format(duration)


class Timers(BasePlugin):
    """Timers"""

    def init(self, *args, **kwargs):
        super(Timers, self).init(*args, **kwargs)
        Commands().register(self)

    def timer(self, target, message):
        self.fire(PRIVMSG(target, message))