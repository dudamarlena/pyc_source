# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/interfaces/client.py
# Compiled at: 2013-01-12 04:21:46
"""Module for client (i.e. user to communication-device) interaction.
The debugged program is at the other end of the communcation."""
import atexit
from import_relative import *
Muser = import_relative('user', top_name='pydbgr')
Mtcpclient = import_relative('tcpclient', '..io', 'pydbgr')
Mfifoclient = import_relative('fifoclient', '..io', 'pydbgr')
Mcomcodes = import_relative('comcodes', '.', 'pydbgr')
Mmisc = import_relative('misc', '..', 'pydbgr')

class ClientInterface(Muser.UserInterface):
    """Interface for a user which is attached to a debugged process
    via some sort of communication medium (e.g. socket, tty, FIFOs).
    This could be on the same computer in a different process or on
    a remote computer."""
    __module__ = __name__
    DEFAULT_INIT_CONNECTION_OPTS = {'IO': 'FIFO'}

    def __init__(self, inp=None, out=None, inout=None, user_opts=None, connection_opts=None):
        get_connection_option = lambda key: Mmisc.option_set(connection_opts, key, self.DEFAULT_INIT_CONNECTION_OPTS)
        Muser.UserInterface.__init__(self, inp, out, user_opts)
        self.inout = None
        if inout:
            self.inout = inout
        else:
            self.server_type = get_connection_option('IO')
            if 'FIFO' == self.server_type:
                self.inout = Mfifoclient.FIFOClient(opts=connection_opts)
            elif 'TCP' == self.server_type:
                self.inout = Mtcpclient.TCPClient(opts=connection_opts)
            else:
                self.errmsg('Expecting server type TCP or FIFO. Got: %s.' % self.server_type)
                return
        return

    def read_remote(self):
        """Send a message back to the server (in contrast to
        the local user output channel)."""
        coded_line = self.inout.read_msg()
        control = coded_line[0]
        remote_line = coded_line[1:]
        return (control, remote_line)

    def write_remote(self, code, msg):
        """Send a message back to the server (in contrast to
        the local user output channel)."""
        return self.inout.writeline(code + msg)


if __name__ == '__main__':
    intf = ClientInterface()