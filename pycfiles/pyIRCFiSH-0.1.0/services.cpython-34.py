# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib64/python3.4/site-packages/PyIRC/extensions/services.py
# Compiled at: 2015-10-08 05:15:23
# Size of source mod 2**32: 3616 bytes
__doc__ = 'Utilities for interacting with IRC services.'
from logging import getLogger
from PyIRC.signal import event
from PyIRC.extensions import BaseExtension
_logger = getLogger(__name__)

class ServicesLogin(BaseExtension):
    """ServicesLogin"""

    def __init__(self, *args, **kwargs):
        """Initalise the ServicesLogin extension.

        :key services_username:
            The username to use for authentication.

        :key services_password:
            The password to use for authentication.

        :key services_idenitfy_fmt:
            A format string using {username} and {password} to send the
            correct message to services.

        :key services_bot:
            The user to send authentication to (defaults to NickServ). Can be
            a full nick!user@host set for the networks that support or require
            this mechanism.

        :key services_command:
            Command to use to authenticate. Defaults to PRIVMSG, but
            NS/NICKSERV are recommended for networks that support it for some
            improved security.

        """
        super().__init__(*args, **kwargs)
        self.base.services_login = self
        self.username = kwargs.get('services_username', self.nick)
        self.password = kwargs.get('services_password')
        self.identify = kwargs.get('services_identify_fmt', 'IDENTIFY {username} {password}')
        self.services_bot = kwargs.get('services_bot', 'NickServ')
        self.services_command = kwargs.get('services_command', 'PRIVMSG')
        self.identify = self.identify.format(username=self.username, password=self.password)
        self.authenticated = False

    @event('commands', 'NOTICE')
    @event('commands', 'PRIVMSG')
    def authenticate(self, _, line):
        """Try to authenticate to services."""
        if self.password is None:
            return
        if self.authenticated or not self.registered:
            return
        _logger.debug('Authenticating to services bot %s with username %s', self.services_bot, self.username)
        if self.services_command.lower() in ('PRIVMSG', 'NOTICE'):
            self.send(self.services_command, [self.services_bot,
             self.identify])
        else:
            self.send(self.services_command, [self.identify])
        self.authenticated = True