# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/ipv6/server/dhcpctl.py
# Compiled at: 2016-12-15 17:28:20
# Size of source mod 2**32: 6103 bytes
"""
The remote control app for the server process
"""
import argparse, logging.handlers, socket, sys
from argparse import ArgumentDefaultsHelpFormatter
from struct import pack
from typing import Iterable, Optional
from dhcpkit.common.logging.verbosity import set_verbosity_logger
logger = logging.getLogger()

class ControlClientError(Exception):
    __doc__ = '\n    Base class for DHCPKit Control Client errors\n    '


class UnknownCommandError(ControlClientError):
    __doc__ = "\n    The server doesn't understand the command we sent\n    "


class WrongServerError(ControlClientError):
    __doc__ = "\n    The socket we connected to doesn't seem to be a DHCPKit server\n    "


class CommunicationError(ControlClientError):
    __doc__ = '\n    There was a problem communicating\n    '


class DHCPKitControlClient:
    __doc__ = '\n    A class for communicating with a DHCPKit DHCPv6 server\n    '

    def __init__(self, control_socket: str):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, pack('ll', 10, 0))
        self.sock.connect(control_socket)
        self.buffer = b''
        line = self.receive_line()
        if not line.startswith('DHCPKit '):
            raise WrongServerError("Socket doesn't seem to be for DHCPKit")

    def receive_line(self, optional: bool=False) -> Optional[str]:
        """
        Receive one line of output from the server

        :param optional: Whether we care about this command being properly executed
        :return: The received line
        """
        if not self.sock:
            if optional:
                return
            raise CommunicationError('Reading from a closed connection')
        while 1:
            parts = self.buffer.split(b'\n', maxsplit=1)
            if len(parts) == 2:
                self.buffer = parts[1]
                return parts[0].decode('utf-8')
            try:
                received = self.sock.recv(1024)
                self.buffer += received
            except OSError:
                if optional:
                    received = b''
                else:
                    raise CommunicationError('No response from server')

            if not received:
                self.sock.close()
                self.sock = None
                return

    def send_command(self, command: str, optional: bool=False):
        """
        Send a command to the server

        :param command: The command
        :param optional: Whether we care about this command being properly executed
        """
        if not self.sock:
            if optional:
                return
            raise CommunicationError('Writing to a closed connection')
        self.sock.send(command.encode('utf-8') + b'\n')

    def execute_command(self, command: str, optional: bool=False) -> Iterable[str]:
        """
        Send a command and parse the response

        :param command: The command
        :param optional: Whether we care about this command being properly executed
        :return: The output
        """
        self.send_command(command, optional=optional)
        while True:
            line = self.receive_line(optional=optional)
            if line is None:
                return ''
            if line == 'UNKNOWN':
                raise UnknownCommandError("Server doesn't understand '{}'".format(command))
            else:
                if line.startswith('OK:'):
                    yield line[3:]
                    return ''
                if line == 'OK':
                    return ''
                yield line


def handle_args(args: Iterable[str]):
    """
    Handle the command line arguments.

    :param args: Command line arguments
    :return: The arguments object
    """
    parser = argparse.ArgumentParser(description='A remote control utility that allows you to send commands to the DHCPv6 server.', formatter_class=ArgumentDefaultsHelpFormatter, epilog="Use the command 'help' to see which commands the server supports.")
    parser.add_argument('command', action='store', help='The command to send to the server')
    parser.add_argument('-v', '--verbosity', action='count', default=0, help='increase output verbosity')
    parser.add_argument('-c', '--control-socket', action='store', metavar='FILENAME', default='/var/run/ipv6-dhcpd.sock', help='location of domain socket for server control')
    args = parser.parse_args(args)
    return args


def main(args: Iterable[str]):
    """
    The main program loop

    :param args: Command line arguments
    :return: The program exit code
    """
    args = handle_args(args)
    set_verbosity_logger(logger, args.verbosity)
    conn = DHCPKitControlClient(args.control_socket)
    output = conn.execute_command(args.command)
    for line in output:
        print(line)

    try:
        output = list(conn.execute_command('quit', optional=True))
        if output:
            raise CommunicationError('Unexpected reply from server: {}'.format(output[0]))
    except BrokenPipeError:
        pass


def run() -> int:
    """
    Run the main program and handle exceptions

    :return: The program exit code
    """
    try:
        main(sys.argv[1:])
        return 0
    except Exception as e:
        logger.critical('Error: {}'.format(e))
        return 1


if __name__ == '__main__':
    sys.exit(run())