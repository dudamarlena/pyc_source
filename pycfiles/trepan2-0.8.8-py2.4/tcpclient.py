# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/inout/tcpclient.py
# Compiled at: 2018-06-25 10:54:26
"""Debugger Socket Input/Output Interface."""
import socket
from trepan.lib import default as Mdefault
from trepan.inout import tcpfns as Mtcpfns
from trepan.inout.base import DebuggerInOutBase
from trepan.misc import option_set

class TCPClient(DebuggerInOutBase):
    """Debugger Client Input/Output Socket."""
    __module__ = __name__
    DEFAULT_INIT_OPTS = {'open': True}

    def __init__(self, inout=None, opts=None):
        get_option = lambda key: option_set(opts, key, Mdefault.CLIENT_SOCKET_OPTS)
        self.inout = None
        self.addr = None
        self.buf = ''
        self.line_edit = False
        self.state = 'disconnected'
        if inout:
            self.inout = inout
        elif get_option('open'):
            self.open(opts)
        return

    def close(self):
        """ Closes both input and output """
        if self.inout:
            self.inout.close()
        self.state = 'disconnnected'

    def open(self, opts=None):
        get_option = lambda key: option_set(opts, key, Mdefault.CLIENT_SOCKET_OPTS)
        HOST = get_option('HOST')
        PORT = get_option('PORT')
        self.inout = None
        for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
            (af, socktype, proto, canonname, sa) = res
            try:
                self.inout = socket.socket(af, socktype, proto)
                self.state = 'connected'
            except socket.error:
                self.inout = None
                self.state = 'disconnected'
                continue

            try:
                self.inout.connect(sa)
            except socket.error:
                self.inout.close()
                self.inout = None
                continue
                break

        if self.inout is None:
            raise IOError('could not open client socket on port %s' % PORT)
        return

    def read_msg(self):
        """Read one message unit. It's possible however that
        more than one message will be set in a receive, so we will
        have to buffer that for the next read.
        EOFError will be raised on EOF.
        """
        if self.state == 'connected':
            if 0 == len(self.buf):
                self.buf = self.inout.recv(Mtcpfns.TCP_MAX_PACKET)
                if 0 == self.buf:
                    self.state = 'disconnected'
                    raise EOFError
            (self.buf, data, length) = Mtcpfns.unpack_msg_segment(self.buf)
            if len(data) == length:
                return data
            while len(data) < length:
                data += self.inout.recv(Mtcpfns.TCP_MAX_PACKET)
                if 0 == self.buf:
                    self.state = 'disconnected'
                    raise EOFError

            self.buf = data[length:]
            data = data[:length]
            return data
        else:
            raise IOError('read_msg called in state: %s.' % self.state)

    def write(self, msg):
        """ This method the debugger uses to write a message unit."""
        return self.inout.send(Mtcpfns.pack_msg(msg))