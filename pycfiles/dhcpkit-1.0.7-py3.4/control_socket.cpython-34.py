# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/ipv6/server/control_socket.py
# Compiled at: 2017-06-08 11:09:29
# Size of source mod 2**32: 5509 bytes
"""
A socket to control the DHCPKit server
"""
import errno, logging, os, socket, time
from typing import List, Optional, Union
import dhcpkit
logger = logging.getLogger(__name__)

class ControlConnection:
    __doc__ = '\n    A connection of the remote control socket\n    '

    def __init__(self, sock: socket.socket):
        logger.debug('Starting new control connection')
        self.sock = sock
        self.buffer = b''
        self.last_activity = time.time()
        self.sock.setblocking(False)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 102400)
        self.send('DHCPKit DHCPv6 Server {}'.format(dhcpkit.__version__))

    def fileno(self) -> int:
        """
        The fileno of the listening socket, so this object can be used by select()

        :return: The file descriptor
        """
        return self.sock.fileno()

    def get_commands(self) -> List[Union[(str, None)]]:
        """
        Receive data until the next newline and return the result

        :return: A list of commands
        """
        received = None
        try:
            received = self.sock.recv(64)
            self.buffer += received
            self.last_activity = time.time()
        except BlockingIOError:
            pass

        if received == b'':
            logger.debug('Control connection closed without saying goodbye')
            return [
             None]
        commands = []
        while 1:
            parts = self.buffer.split(b'\n', maxsplit=1)
            if len(parts) < 2:
                break
            self.buffer = parts[1]
            try:
                command = parts[0].decode('utf-8').lower()
            except UnicodeError:
                continue

            if command:
                commands.append(command)
                continue

        return commands

    def send(self, output: str, eol=b'\n'):
        """
        Send data over the socket

        :param output: The data to send
        :param eol: The end-of-line character
        """
        try:
            self.sock.send(output.encode('utf-8') + eol)
        except BrokenPipeError:
            pass

    def close(self):
        """
        Close the socket nicely
        """
        logger.debug('Closing control connection')
        self.sock.close()

    def acknowledge(self, feedback: str=None):
        """
        Acknowledge the command
        """
        if feedback:
            self.send('OK: {}'.format(feedback))
        else:
            self.send('OK')

    def reject(self):
        """
        Reject the command
        """
        self.send('UNKNOWN')


class ControlSocket:
    __doc__ = '\n    Remote control of the DHCPKit server\n    '

    def __init__(self, socket_path: str):
        self.socket_path = socket_path
        self.listen_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.listen_socket.setblocking(False)
        try:
            logger.info('Creating control socket {}'.format(socket_path))
            self.listen_socket.bind(socket_path)
        except FileNotFoundError:
            raise RuntimeError("The path to control socket {} doesn't exist".format(socket_path)) from None
        except OSError as e:
            if e.errno == errno.EADDRINUSE:
                logger.debug("Control socket at {} exists, trying to see if it's still alive".format(socket_path))
                try:
                    test_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                    test_socket.connect(socket_path)
                except OSError as e2:
                    if e2.errno == errno.ECONNREFUSED:
                        logger.debug('Replacing old control socket {}'.format(socket_path))
                        os.unlink(socket_path)
                        self.listen_socket.bind(socket_path)
                    elif e2.errno == errno.ENOTSOCK:
                        raise RuntimeError('Control socket {} is unusable'.format(socket_path)) from None

        if not self.listen_socket.getsockname():
            raise RuntimeError('Cannot create control socket {}'.format(socket_path)) from None
        self.listen_socket.listen(32)

    def close(self):
        """
        Close the socket nicely
        """
        self.listen_socket.close()

    def fileno(self) -> int:
        """
        The fileno of the listening socket, so this object can be used by select()

        :return: The file descriptor
        """
        return self.listen_socket.fileno()

    def accept(self) -> Optional[ControlConnection]:
        """
        Accept a new connection

        :return: The new connection
        """
        try:
            sock = self.listen_socket.accept()[0]
            return ControlConnection(sock)
        except OSError:
            logger.debug('Control connection broken after connecting, ignoring')
            return