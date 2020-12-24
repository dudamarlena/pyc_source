# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/io/tcpclient.py
# Compiled at: 2013-03-23 12:47:09
"""Debugger Socket Input/Output Interface. """
import socket
from import_relative import import_relative
Mbase_io = import_relative('base_io', top_name='pydbgr')
Mdefault = import_relative('default', '..lib', 'pydbgr')
Mmisc = import_relative('misc', '..', 'pydbgr')
Mtcpfns = import_relative('tcpfns', '.', 'pydbgr')

class TCPClient(Mbase_io.DebuggerInOutBase):
    """Debugger Client Input/Output Socket."""
    __module__ = __name__
    DEFAULT_INIT_OPTS = {'open': True}

    def __init__(self, inout=None, opts=None):
        get_option = lambda key: Mmisc.option_set(opts, key, Mdefault.CLIENT_SOCKET_OPTS)
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
        get_option = lambda key: Mmisc.option_set(opts, key, Mdefault.CLIENT_SOCKET_OPTS)
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
            (self.buf, data) = Mtcpfns.unpack_msg(self.buf)
            return data
        else:
            raise IOError('read_msg called in state: %s.' % self.state)

    def write(self, msg):
        """ This method the debugger uses to write a message unit."""
        return self.inout.send(Mtcpfns.pack_msg(msg))


if __name__ == '__main__':
    inout = TCPClient(opts={'open': False})
    import sys
    if len(sys.argv) > 1:
        print 'Connecting...',
        inout.open()
        print 'connected.'
        while True:
            line = raw_input('nu? ')
            if len(line) == 0:
                break
            try:
                line = inout.writeline(line)
                print ('Got: ', inout.read_msg().rstrip('\n'))
            except EOFError:
                break

    inout.close()