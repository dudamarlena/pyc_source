# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.4/site-packages/PyIRC/extensions/ctcp.py
# Compiled at: 2015-10-09 06:57:46
# Size of source mod 2**32: 2521 bytes
"""Client to Client Protocol extensions and events."""
from logging import getLogger
from PyIRC.signal import event
from PyIRC.extensions import BaseExtension
from PyIRC.auxparse import CTCPMessage
from PyIRC.util.version import versionstr
_logger = getLogger(__name__)

class CTCP(BaseExtension):
    __doc__ = 'Add CTCP dispatch functionaltiy.\n\n    Hooks may be added by having a commands_ctcp or commands_nctcp\n    mapping in your base class.\n\n    '
    default_version = 'Powered by PyIRC v{}'.format(versionstr)

    def __init__(self, *args, **kwargs):
        """Initalise the CTCP extension.

        :key ctcp_version:
            Version string to use, defaults to default_version.

        """
        super().__init__(*args, **kwargs)
        self.version = kwargs.get('ctcp_version', self.default_version)

    def ctcp(self, target, command, param=None):
        """CTCP a target a given command."""
        ctcp = CTCPMessage('PRIVMSG', command.upper(), target, param)
        line = ctcp.line
        self.send(line.command, line.params)

    def nctcp(self, target, command, param=None):
        """Reply to a CTCP."""
        ctcp = CTCPMessage('NOTICE', command.upper(), target, param)
        line = ctcp.line
        self.send(line.command, line.params)

    @event('commands', 'PRIVMSG')
    def ctcp_in(self, _, line):
        """Check message for CTCP (incoming) and dispatch if necessary."""
        ctcp = CTCPMessage.parse(line)
        if not ctcp:
            return
        command = ctcp.command
        self.call_event('commands_ctcp', command, ctcp, line)

    @event('commands', 'NOTICE')
    def nctcp_in(self, _, line):
        """Check message for NCTCP (incoming) and dispatch if necessary."""
        ctcp = CTCPMessage.parse(line)
        if not ctcp:
            return
        command = ctcp.command
        self.call_event('commands_ctcp', command, ctcp, line)

    @event('commands_ctcp', 'PING')
    def c_ping(self, _, ctcp, line):
        """Respond to CTCP ping."""
        self.nctcp(ctcp.target, 'PING', ctcp.param)

    @event('commands_ctcp', 'VERSION')
    def c_version(self, _, ctcp, line):
        """Respond to CTCP version."""
        self.nctcp(ctcp.target, 'VERSION', self.version)