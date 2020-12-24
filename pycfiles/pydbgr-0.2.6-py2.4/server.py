# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/interfaces/server.py
# Compiled at: 2013-01-12 04:23:38
"""Module for Server (i.e. program to communication-device) interaction"""
import atexit, os
from import_relative import *
Minterface = import_relative('interface', '..', 'pydbgr')
Mtcpserver = import_relative('tcpserver', '..io', 'pydbgr')
Mfifoserver = import_relative('fifoserver', '..io', 'pydbgr')
Mmisc = import_relative('misc', '..', 'pydbgr')
Mcomcodes = import_relative('comcodes', '.', 'pydbgr')

class ServerInterface(Minterface.DebuggerInterface):
    """Interface for debugging a program but having user control
    reside outside of the debugged process, possibly on another
    computer."""
    __module__ = __name__
    DEFAULT_INIT_CONNECTION_OPTS = {'IO': 'TCP'}

    def __init__(self, inout=None, out=None, connection_opts=None):
        get_option = lambda key: Mmisc.option_set(connection_opts, key, self.DEFAULT_INIT_CONNECTION_OPTS)
        atexit.register(self.finalize)
        self.inout = None
        if inout:
            self.inout = inout
        else:
            self.server_type = get_option('IO')
            if 'FIFO' == self.server_type:
                self.inout = Mfifoserver.FIFOServer()
            else:
                self.inout = Mtcpserver.TCPServer()
        self.output = inout
        self.input = inout
        self.interactive = True
        return

    def close(self):
        """ Closes both input and output """
        if self.inout:
            self.inout.close()

    def confirm(self, prompt, default):
        """ Called when a dangerous action is about to be done to make sure
        it's okay. `prompt' is printed; user response is returned."""
        while True:
            try:
                self.write_confirm(prompt, default)
                reply = self.readline('').strip().lower()
            except EOFError:
                return default

            if reply in ('y', 'yes'):
                return True
            elif reply in ('n', 'no'):
                return False
            else:
                self.msg('Please answer y or n.')

        return default

    def errmsg(self, str, prefix='** '):
        """Common routine for reporting debugger error messages.
           """
        return self.msg('%s%s' % (prefix, str))

    def finalize(self, last_wishes=Mcomcodes.QUIT):
        if self.is_connected():
            self.inout.writeline(last_wishes)
        self.close()

    def is_connected(self):
        """ Return True if we are connected """
        return 'connected' == self.inout.state

    def msg(self, msg):
        """ used to write to a debugger that is connected to this
        server; `str' written will have a newline added to it
        """
        self.inout.writeline(Mcomcodes.PRINT + msg)

    def msg_nocr(self, msg):
        """ used to write to a debugger that is connected to this
        server; `str' written will not have a newline added to it
        """
        self.inout.write(Mcomcodes.PRINT + msg)

    def read_command(self, prompt):
        return self.readline(prompt)

    def read_data(self):
        return self.inout.read_data()

    def readline(self, prompt, add_to_history=True):
        if prompt:
            self.write_prompt(prompt)
        coded_line = self.inout.read_msg()
        self.read_ctrl = coded_line[0]
        return coded_line[1:]

    def state(self):
        """ Return connected """
        return self.inout.state

    def write_prompt(self, prompt):
        return self.inout.writeline(Mcomcodes.PROMPT + prompt)

    def write_confirm(self, prompt, default):
        if default:
            code = Mcomcodes.CONFIRM_TRUE
        else:
            code = Mcomcodes.CONFIRM_FALSE
        return self.inout.writeline(code + prompt)


if __name__ == '__main__':
    intf = ServerInterface()