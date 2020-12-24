# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/inout/tcpserver.py
# Compiled at: 2020-04-27 23:16:57
"""Debugger Server Input/Output interface. """
import socket, errno
from trepan.lib import default as Mdefault
from trepan import misc as Mmisc
from trepan.inout import tcpfns as Mtcpfns
from trepan.inout.base import DebuggerInOutBase

class TCPServer(DebuggerInOutBase):
    """Debugger Server Input/Output Socket."""
    DEFAULT_INIT_OPTS = {'open': True, 'socket': None}

    def __init__(self, inout=None, opts=None):
        get_option = lambda key: Mmisc.option_set(opts, key, self.DEFAULT_INIT_OPTS)
        self.inout = None
        self.conn = None
        self.addr = None
        self.remote_addr = ''
        self.buf = ''
        self.line_edit = False
        self.state = 'disconnected'
        self.PORT = None
        self.HOST = None
        if inout:
            self.inout = inout
        if get_option('socket'):
            self.inout = opts['socket']
            self.inout.listen(1)
            self.state = 'listening'
        elif get_option('open'):
            self.open(opts)
        return

    def close(self):
        """ Closes both socket and server connection. """
        self.state = 'closing'
        if self.inout:
            self.inout.close()
        self.state = 'closing connection'
        if self.conn:
            self.conn.close()
        self.state = 'disconnected'

    def open(self, opts=None):
        get_option = lambda key: Mmisc.option_set(opts, key, Mdefault.SERVER_SOCKET_OPTS)
        self.HOST = get_option('HOST')
        self.PORT = get_option('PORT')
        self.reuse = get_option('reuse')
        self.search_limit = get_option('search_limit')
        self.inout = None
        this_port = self.PORT - 1
        for i in range(self.search_limit):
            this_port += 1
            for res in socket.getaddrinfo(self.HOST, this_port, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
                (af, socktype, proto, canonname, sa) = res
                try:
                    self.inout = socket.socket(af, socktype, proto)
                except socket.error:
                    self.inout = None
                    continue

                try:
                    if get_option('reuse'):
                        self.inout.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    self.inout.bind(sa)
                    self.inout.listen(1)
                    self.state = 'listening'
                    break
                except socket.error, exc:
                    if exc.errno in [errno.EADDRINUSE, errno.EINVAL]:
                        self.inout.close()
                        self.inout = None
                        continue
                    raise

            if self.state == 'listening':
                break

        if self.inout is None:
            raise IOError('could not open server socket after trying ports %s..%s' % (
             self.PORT, this_port))
        self.PORT = this_port
        return

    def read(self):
        if len(self.buf) == 0:
            self.read_msg()
        return self.buf

    def read_msg(self):
        """Read one message unit. It's possible however that
        more than one message will be set in a receive, so we will
        have to buffer that for the next read.
        EOFError will be raised on EOF.
        """
        if self.state != 'connected':
            self.wait_for_connect()
        if self.state == 'connected':
            if 0 == len(self.buf):
                self.buf = self.conn.recv(Mtcpfns.TCP_MAX_PACKET)
                if 0 == len(self.buf):
                    self.state = 'disconnected'
                    raise EOFError
            (self.buf, data) = Mtcpfns.unpack_msg(self.buf)
            return data
        raise IOError('read_msg called in state: %s.' % self.state)

    def wait_for_connect(self):
        (self.conn, self.addr) = self.inout.accept()
        self.remote_addr = (':').join(str(v) for v in self.addr)
        self.state = 'connected'

    def write(self, msg):
        """ This method the debugger uses to write. In contrast to
        writeline, no newline is added to the end to `str'. Also
        msg doesn't have to be a string.
        """
        if self.state != 'connected':
            self.wait_for_connect()
        buffer = Mtcpfns.pack_msg(msg)
        while len(buffer) > Mtcpfns.TCP_MAX_PACKET:
            self.conn.send(buffer[:Mtcpfns.TCP_MAX_PACKET])
            buffer = buffer[Mtcpfns.TCP_MAX_PACKET:]

        return self.conn.send(buffer)


if __name__ == '__main__':
    inout = TCPServer(opts={'open': False})
    import sys
    if len(sys.argv) > 1:
        inout.open()
        print 'Listening for connection on %s:%s' % (
         inout.HOST, inout.PORT)
        while True:
            try:
                line = inout.read_msg().rstrip('\n')
                print line
                inout.writeline('ack: ' + line)
            except EOFError:
                break

    inout.close()