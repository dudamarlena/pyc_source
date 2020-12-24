# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.4/site-packages/PyIRC/extensions/starttls.py
# Compiled at: 2015-10-08 05:15:23
# Size of source mod 2**32: 2394 bytes
"""Automatic SSL negotiation.

It's a little like the ESMTP STARTTLS command, but the server does not
forget all of the client state after it is issued. Therefore, it should
be issued as quickly as possible.

"""
from logging import getLogger
from taillight.signal import SignalDefer
from PyIRC.signal import event
from PyIRC.extensions import BaseExtension
from PyIRC.numerics import Numerics
_logger = getLogger(__name__)

class StartTLS(BaseExtension):
    __doc__ = 'Support for the STARTTLS extension.\n\n    Not all I/O backends support this, notably :py:class:`~PyIRC.io.asyncio`.\n\n    '
    requires = [
     'CapNegotiate']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tls_event = None
        if not self.ssl:
            self.caps = {'tls': []}

    @event('link', 'disconnected')
    def close(self, _):
        """Reset state because we are disconnected."""
        self.tls_event = None

    @event('cap_perform', 'ack', priority=-1000)
    def starttls(self, _, line, caps):
        """Respond to TLS CAP acknowledgement."""
        if self.ssl:
            return
        if self.tls_event:
            return
        if 'tls' in caps:
            self.tls_event = event
            self.send('STARTTLS', None)
            raise SignalDefer()

    @event('commands', Numerics.RPL_STARTTLS)
    def wrap(self, _, line):
        """Actually start TLS communication."""
        _logger.info('Performing STARTTLS initiation...')
        self.wrap_ssl()
        self.resume_event('cap_perform', 'ack')

    @event('commands', Numerics.ERR_STARTTLS)
    def abort(self, _, line):
        """Report a problem with TLS communication.

        .. warning::
            This allows connection to continue anyway!
        """
        _logger.critical('STARTTLS initiation failed, connection not secure')
        self.resume_event('cap_perform', 'ack')