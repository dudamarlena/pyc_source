# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/contrib/telnet/server.py
# Compiled at: 2019-08-15 23:53:39
# Size of source mod 2**32: 12900 bytes
"""
Telnet server.

Example usage::

    class MyTelnetApplication(TelnetApplication):
        def client_connected(self, telnet_connection):
            # Set CLI with simple prompt.
            telnet_connection.set_application(
                telnet_connection.create_prompt_application(...))

        def handle_command(self, telnet_connection, document):
            # When the client enters a command, just reply.
            telnet_connection.send('You said: %r

' % document.text)

        ...

    a = MyTelnetApplication()
    TelnetServer(application=a, host='127.0.0.1', port=23).run()
"""
from __future__ import unicode_literals
import socket, select, threading, os, fcntl
from six import int2byte, text_type, binary_type
from codecs import getincrementaldecoder
from prompt_tool_kit.enums import DEFAULT_BUFFER
from prompt_tool_kit.eventloop.base import EventLoop
from prompt_tool_kit.interface import CommandLineInterface, Application
from prompt_tool_kit.layout.screen import Size
from prompt_tool_kit.shortcuts import create_prompt_application
from prompt_tool_kit.terminal.vt100_input import InputStream
from prompt_tool_kit.terminal.vt100_output import Vt100_Output
from .log import logger
from .protocol import IAC, DO, LINEMODE, SB, MODE, SE, WILL, ECHO, NAWS, SUPPRESS_GO_AHEAD
from .protocol import TelnetProtocolParser
from .application import TelnetApplication
__all__ = ('TelnetServer', )

def _initialize_telnet(connection):
    logger.info('Initializing telnet connection')
    connection.send(IAC + DO + LINEMODE)
    connection.send(IAC + WILL + SUPPRESS_GO_AHEAD)
    connection.send(IAC + SB + LINEMODE + MODE + int2byte(0) + IAC + SE)
    connection.send(IAC + WILL + ECHO)
    connection.send(IAC + DO + NAWS)


class _ConnectionStdout(object):
    __doc__ = '\n    Wrapper around socket which provides `write` and `flush` methods for the\n    Vt100_Output output.\n    '

    def __init__(self, connection, encoding):
        self._encoding = encoding
        self._connection = connection
        self._buffer = []

    def write(self, data):
        assert isinstance(data, text_type)
        self._buffer.append(data.encode(self._encoding))
        self.flush()

    def flush(self):
        try:
            self._connection.send((b'').join(self._buffer))
        except socket.error as e:
            logger.error("Couldn't send data over socket: %s" % e)

        self._buffer = []


class TelnetConnection(object):
    __doc__ = '\n    Class that represents one Telnet connection.\n    '

    def __init__(self, conn, addr, application, server, encoding):
        if not isinstance(addr, tuple):
            raise AssertionError
        else:
            if not isinstance(application, TelnetApplication):
                raise AssertionError
            elif not isinstance(server, TelnetServer):
                raise AssertionError
            assert isinstance(encoding, text_type)
        self.conn = conn
        self.addr = addr
        self.application = application
        self.closed = False
        self.handling_command = True
        self.server = server
        self.encoding = encoding
        self.callback = None
        self.size = Size(rows=40, columns=79)
        _initialize_telnet(conn)

        def get_size():
            return self.size

        self.stdout = _ConnectionStdout(conn, encoding=encoding)
        self.vt100_output = Vt100_Output((self.stdout), get_size, write_binary=False)
        self.eventloop = _TelnetEventLoopInterface(server)
        self.set_application(create_prompt_application())
        application.client_connected(self)
        self.handling_command = False
        self.cli._redraw()

    def set_application(self, app, callback=None):
        """
        Set ``CommandLineInterface`` instance for this connection.
        (This can be replaced any time.)

        :param cli: CommandLineInterface instance.
        :param callback: Callable that takes the result of the CLI.
        """
        assert isinstance(app, Application)
        if not callback is None:
            if not callable(callback):
                raise AssertionError
        self.cli = CommandLineInterface(application=app,
          eventloop=(self.eventloop),
          output=(self.vt100_output))
        self.callback = callback
        cb = self.cli.create_eventloop_callbacks()
        inputstream = InputStream(cb.feed_key)
        stdin_decoder_cls = getincrementaldecoder(self.encoding)
        stdin_decoder = [stdin_decoder_cls()]
        self.cli._is_running = True

        def data_received(data):
            assert isinstance(data, binary_type)
            try:
                result = stdin_decoder[0].decode(data)
                inputstream.feed(result)
            except UnicodeDecodeError:
                stdin_decoder[0] = stdin_decoder_cls()
                return ''

        def size_received(rows, columns):
            self.size = Size(rows=rows, columns=columns)
            cb.terminal_size_changed()

        self.parser = TelnetProtocolParser(data_received, size_received)

    def feed(self, data):
        """
        Handler for incoming data. (Called by TelnetServer.)
        """
        assert isinstance(data, binary_type)
        self.parser.feed(data)
        self.cli._redraw()
        if self.cli.is_returning:
            try:
                return_value = self.cli.return_value()
            except (EOFError, KeyboardInterrupt) as e:
                logger.info('%s, closing connection.', type(e).__name__)
                self.close()
                return

            self._handle_command(return_value)

    def _handle_command(self, command):
        """
        Handle command. This will run in a separate thread, in order not
        to block the event loop.
        """
        logger.info('Handle command %r', command)

        def in_executor():
            self.handling_command = True
            try:
                if self.callback is not None:
                    self.callback(self, command)
            finally:
                self.server.call_from_executor(done)

        def done():
            self.handling_command = False
            if not self.closed:
                self.cli.reset()
                self.cli.buffers[DEFAULT_BUFFER].reset()
                self.cli.renderer.request_absolute_cursor_position()
                self.vt100_output.flush()
                self.cli._redraw()

        self.server.run_in_executor(in_executor)

    def erase_screen(self):
        """
        Erase output screen.
        """
        self.vt100_output.erase_screen()
        self.vt100_output.cursor_goto(0, 0)
        self.vt100_output.flush()

    def send(self, data):
        """
        Send text to the client.
        """
        assert isinstance(data, text_type)
        self.stdout.write(data.replace('\n', '\r\n'))
        self.stdout.flush()

    def close(self):
        """
        Close the connection.
        """
        self.application.client_leaving(self)
        self.conn.close()
        self.closed = True


class _TelnetEventLoopInterface(EventLoop):
    __doc__ = '\n    Eventloop object to be assigned to `CommandLineInterface`.\n    '

    def __init__(self, server):
        self._server = server

    def close(self):
        """ Ignore. """
        pass

    def stop(self):
        """ Ignore. """
        pass

    def run_in_executor(self, callback):
        self._server.run_in_executor(callback)

    def call_from_executor(self, callback, _max_postpone_until=None):
        self._server.call_from_executor(callback)

    def add_reader(self, fd, callback):
        raise NotImplementedError

    def remove_reader(self, fd):
        raise NotImplementedError


class TelnetServer(object):
    __doc__ = '\n    Telnet server implementation.\n    '

    def __init__(self, host='127.0.0.1', port=23, application=None, encoding='utf-8'):
        if not isinstance(host, text_type):
            raise AssertionError
        else:
            if not isinstance(port, int):
                raise AssertionError
            elif not isinstance(application, TelnetApplication):
                raise AssertionError
            assert isinstance(encoding, text_type)
        self.host = host
        self.port = port
        self.application = application
        self.encoding = encoding
        self.connections = set()
        self._calls_from_executor = []
        self._schedule_pipe = os.pipe()
        fcntl.fcntl(self._schedule_pipe[0], fcntl.F_SETFL, os.O_NONBLOCK)

    @classmethod
    def create_socket(cls, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(4)
        return s

    def run_in_executor(self, callback):
        threading.Thread(target=callback).start()

    def call_from_executor(self, callback):
        self._calls_from_executor.append(callback)
        if self._schedule_pipe:
            os.write(self._schedule_pipe[1], b'x')

    def _process_callbacks(self):
        """
        Process callbacks from `call_from_executor` in eventloop.
        """
        os.read(self._schedule_pipe[0], 1024)
        calls_from_executor, self._calls_from_executor = self._calls_from_executor, []
        for c in calls_from_executor:
            c()

    def run(self):
        """
        Run the eventloop for the telnet server.
        """
        listen_socket = self.create_socket(self.host, self.port)
        logger.info('Listening for telnet connections on %s port %r', self.host, self.port)
        try:
            while True:
                self.connections = set([c for c in self.connections if not c.closed])
                connections = set([c for c in self.connections if not c.handling_command])
                read_list = [
                 listen_socket, self._schedule_pipe[0]] + [c.conn for c in connections]
                read, _, _ = select.select(read_list, [], [])
                for s in read:
                    if s == listen_socket:
                        self._accept(listen_socket)
                    else:
                        if s == self._schedule_pipe[0]:
                            self._process_callbacks()
                        else:
                            self._handle_incoming_data(s)

        finally:
            listen_socket.close()

    def _accept(self, listen_socket):
        """
        Accept new incoming connection.
        """
        conn, addr = listen_socket.accept()
        connection = TelnetConnection(conn, addr, (self.application), self, encoding=(self.encoding))
        self.connections.add(connection)
        (logger.info)(*('New connection %r %r', ), *addr)

    def _handle_incoming_data(self, conn):
        """
        Handle incoming data on socket.
        """
        connection = [c for c in self.connections if c.conn == conn][0]
        data = conn.recv(1024)
        if data:
            connection.feed(data)
        else:
            self.connections.remove(connection)