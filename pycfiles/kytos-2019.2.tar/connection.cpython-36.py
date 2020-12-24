# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/humberto/src/kytos/kytos-asyncio/kytos/core/connection.py
# Compiled at: 2019-06-06 13:59:39
# Size of source mod 2**32: 4718 bytes
"""Module with main classes related to Connections."""
import logging
from enum import Enum
from errno import EBADF, ENOTCONN
from socket import SHUT_RDWR
from socket import error as SocketError
__all__ = ('Connection', 'ConnectionProtocol', 'ConnectionState')
LOG = logging.getLogger(__name__)

class ConnectionState(Enum):
    __doc__ = 'Enum of possible general connections states.'
    NEW = 0
    SETUP = 1
    ESTABLISHED = 2
    FAILED = 3
    FINISHED = 4


class ConnectionProtocol:
    __doc__ = 'Class to hold simple protocol information for the connection.'

    def __init__(self, name=None, version=None, state=None):
        """Assign parameters to instance variables."""
        self.name = name
        self.version = version
        self.state = state


class Connection:
    __doc__ = 'Connection class to abstract a network connections.'

    def __init__(self, address, port, socket, switch=None):
        """Assign parameters to instance variables.

        Args:
            address (|hw_address|): Source address.
            port (int): Port number.
            socket (socket): socket.
            switch (:class:`~.Switch`): switch with this connection.
        """
        self.address = address
        self.port = port
        self.socket = socket
        self.switch = switch
        self.state = ConnectionState.NEW
        self.protocol = ConnectionProtocol()
        self.remaining_data = b''

    def __str__(self):
        return f"Connection({self.address!r}, {self.port!r})"

    def __repr__(self):
        return f"Connection({self.address!r}, {self.port!r}," + f" {self.socket!r}, {self.switch!r}, {self.state!r})"

    @property
    def state(self):
        """Return the state of the connection."""
        return self._state

    @state.setter
    def state(self, new_state):
        if new_state not in ConnectionState:
            raise Exception('Unknown State', new_state)
        self._state = new_state
        LOG.debug('Connection %s changed state: %s', self.id, self.state)

    @property
    def id(self):
        """Return id from Connection instance.

        Returns:
            string: Connection id.

        """
        return (
         self.address, self.port)

    def send(self, buffer):
        """Send a buffer message using the socket from the connection instance.

        Args:
            buffer (bytes): Message buffer that will be sent.
        """
        try:
            if self.is_alive():
                self.socket.sendall(buffer)
        except (OSError, SocketError) as exception:
            LOG.debug('Could not send packet. Exception: %s', exception)
            self.close()

    def close(self):
        """Close the socket from connection instance."""
        self.state = ConnectionState.FINISHED
        if self.switch:
            if self.switch.connection is self:
                self.switch.connection = None
        LOG.debug('Shutting down Connection %s', self.id)
        try:
            self.socket.shutdown(SHUT_RDWR)
            self.socket.close()
            self.socket = None
            LOG.debug('Connection Closed: %s', self.id)
        except OSError as exception:
            if exception.errno not in (ENOTCONN, EBADF):
                raise exception
        except AttributeError as exception:
            LOG.debug('Socket Already Closed: %s', self.id)

    def is_alive(self):
        """Return True if the connection socket is alive. False otherwise."""
        return self.socket is not None and self.state not in (
         ConnectionState.FINISHED, ConnectionState.FAILED)

    def is_new(self):
        """Return True if the connection is new. False otherwise."""
        return self.state == ConnectionState.NEW

    def is_established(self):
        """Return True if the connection is established. False otherwise."""
        return self.state == ConnectionState.ESTABLISHED

    def is_during_setup(self):
        """Return True if the connection is in setup state. False otherwise."""
        return self.state == ConnectionState.SETUP

    def set_established_state(self):
        """Set the connection state to Established."""
        self.state = ConnectionState.ESTABLISHED

    def set_setup_state(self):
        """Set the connection state to Setup."""
        self.state = ConnectionState.SETUP

    def update_switch(self, switch):
        """Update switch with this instance of Connection.

        Args:
          switch (:class:`~.Switch`): switch instance.
        """
        self.switch = switch
        self.switch.connection = self