# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/interfaces/client.py
# Compiled at: 2017-08-12 23:13:24
"""Module for client (i.e. user to communication-device) interaction.
The debugged program is at the other end of the communcation."""
from trepan.interfaces import user as Muser
from trepan.inout import tcpclient as Mtcpclient, fifoclient as Mfifoclient
DEFAULT_INIT_CONNECTION_OPTS = {'IO': 'TCP'}

class ClientInterface(Muser.UserInterface):
    """Interface for a user which is attached to a debugged process
    via some sort of communication medium (e.g. socket, tty, FIFOs).
    This could be on the same computer in a different process or on
    a remote computer."""

    def __init__(self, inp=None, out=None, inout=None, user_opts={}, connection_opts={}):
        opts = DEFAULT_INIT_CONNECTION_OPTS.copy()
        opts.update(connection_opts)
        Muser.UserInterface.__init__(self, inp, out, user_opts)
        self.inout = None
        if inout:
            self.inout = inout
        else:
            self.server_type = opts['IO']
            if 'FIFO' == self.server_type:
                self.inout = Mfifoclient.FIFOClient(opts=opts)
            elif 'TCP' == self.server_type:
                self.inout = Mtcpclient.TCPClient(opts=opts)
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