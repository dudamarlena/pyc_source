# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/io/tcpserver.py
# Compiled at: 2013-03-23 12:47:17
__doc__ = 'Debugger Server Input/Output interface. '
import socket
from import_relative import import_relative
Mbase_io = import_relative('base_io', top_name='pydbgr')
Mdefault = import_relative('default', '..lib', top_name='pydbgr')
Mmisc = import_relative('misc', '..', 'pydbgr')
Mtcpfns = import_relative('tcpfns', '.', 'pydbgr')

class TCPServer(Mbase_io.DebuggerInOutBase):
    """Debugger Server Input/Output Socket."""
    __module__ = __name__
    DEFAULT_INIT_OPTS = {'open': True}

    def __init__(self, inout=None, opts=None):
        get_option = lambda key: Mmisc.option_set(opts, key, self.DEFAULT_INIT_OPTS)
        self.inout = None
        self.conn = None
        self.addr = None
        self.buf = ''
        self.state = 'disconnected'
        self.PORT = None
        self.HOST = None
        if inout:
            self.inout = inout
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
        self.inout = None
        for res in socket.getaddrinfo(self.HOST, self.PORT, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
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
            except socket.error:
                self.inout.close()
                self.inout = None
                continue

            break

        if self.inout is None:
            raise IOError('could not open server socket on port %s' % self.PORT)
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
        else:
            raise IOError('read_msg called in state: %s.' % self.state)

    def wait_for_connect(self):
        (self.conn, self.addr) = self.inout.accept()
        self.state = 'connected'

    def write(self, msg):
        """ This method the debugger uses to write. In contrast to
        writeline, no newline is added to the end to `str'. Also
        msg doesn't have to be a string.
        """
        if self.state != 'connected':
            self.wait_for_connect()
        return self.conn.send(Mtcpfns.pack_msg(msg))


if __name__ == '__main__':
    inout = TCPServer(opts={'open': False})
    import sys
    if len(sys.argv) > 1:
        print 'Listening for connection...'
        inout.open()
        while True:
            try:
                line = inout.read_msg().rstrip('\n')
                print line
                inout.writeline('ack: ' + line)
            except EOFError:
                break

    inout.close()