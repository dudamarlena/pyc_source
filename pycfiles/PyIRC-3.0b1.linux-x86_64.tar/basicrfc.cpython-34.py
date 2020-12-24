# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.4/site-packages/PyIRC/extensions/basicrfc.py
# Compiled at: 2015-10-08 20:55:01
# Size of source mod 2**32: 3643 bytes
"""Bare minimum IRC RFC standards support."""
from logging import getLogger
from PyIRC.signal import event
from PyIRC.numerics import Numerics
from PyIRC.extensions import BaseExtension
_logger = getLogger(__name__)

class BasicRFC(BaseExtension):
    __doc__ = 'Basic RFC1459 support.\n\n    This is basically just a module that ensures your bot doesn\'t time out and\n    can track its own nick. Nobody is making you use this implementation, but\n    it is highly recommended.\n\n    This extension adds ``base.basic_rfc`` as itself as an alias for\n    ``get_extension("BasicRFC").``.\n\n    :ivar nick:\n        Our present real nickname as reported by the IRC server.\n\n    :ivar prev_nick:\n        If we get a NICK event from the server, and it\'s for us, our last nick\n        will be stored here. Useful in case of services collisions that change\n        our nick, SANICK/FORCENICK operator abuse, or another extension\n        changes our nick.\n\n    '

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base.basic_rfc = self
        self.prev_nick = None
        self.nick = self.base.nick
        self.registered = False
        self.server_version = (
         None, [])

    @event('link', 'connected')
    def handshake(self, _):
        """Register with the server."""
        if not self.registered:
            if self.server_password:
                self.send('PASS', [self.server_password])
            self.send('NICK', [self.nick])
            self.send('USER', [self.username, '*', '*',
             self.gecos])

    @event('link', 'disconnected')
    def disconnected(self, _):
        """Reset our state since we are disconnected now."""
        self.connected = False
        self.registered = False
        self.nick = self.base.nick
        self.prev_nick = None
        self.server_version = (None, [])

    @event('commands', Numerics.RPL_HELLO)
    @event('commands', 'NOTICE')
    def on_connected(self, _, line):
        """Notate that we are successfully connected now."""
        self.connected = True

    @event('commands', 'PING')
    def pong(self, _, line):
        """Respond to server PING."""
        self.send('PONG', line.params)

    @event('commands', 'NICK')
    def on_nick(self, _, line):
        """Possibly update our nick, if we're the ones changing."""
        if line.hostmask.nick != self.nick:
            return
        self.prev_nick = self.nick
        self.nick = line.params[0]

    @event('commands_out', 'NICK')
    def on_nick_out(self, _, line):
        """Update our nick during registration.

        Since nothing is sent back during registration, this needs to be a
        special case.

        ..note::
            :py:attr:`~PyIRC.extensions.basicrfc.BasicRFC.prev_nick` is not
            set by this hook.
        """
        if not self.registered:
            self.nick = line.params[0]

    @event('commands', Numerics.RPL_WELCOME)
    def welcome(self, _, line):
        """Notate that we are successfully registered now."""
        self.registered = True
        self.send('VERSION', [])

    @event('commands', Numerics.RPL_VERSION)
    def version(self, _, line):
        """Process the server version information."""
        self.server_version = (
         line.params[1], line.params[2:])