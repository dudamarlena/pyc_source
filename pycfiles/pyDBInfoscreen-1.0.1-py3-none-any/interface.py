# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/interface.py
# Compiled at: 2013-01-12 04:21:24
__doc__ = 'A base class for a debugger interface.'
import sys
NotImplementedMessage = 'This method must be overriden in a subclass'
__all__ = [
 'DebuggerInterface']

class DebuggerInterface:
    """
A debugger interface handles the communication or interaction with between
the program and the outside portion which could be
    - a user, 
    - a front-end that talks to a user, or
    - another interface in another process or computer
    """
    __module__ = __name__

    def __init__(self, inp=None, out=None):
        self.input = inp or sys.stdin
        self.output = out or sys.stdout
        self.interactive = False

    def close(self):
        """ Closes all input and/or output """
        raise NotImplementedError, NotImplementedMessage

    def confirm(self, prompt, default):
        """ Called when a dangerous action is about to be done to make sure
        it's okay. `prompt' is printed; user response is returned."""
        raise NotImplementedError, NotImplementedMessage

    def errmsg(self, str, prefix='** '):
        """Common routine for reporting debugger error messages.
           """
        raise NotImplementedError, NotImplementedMessage

    def finalize(self, last_wishes=None):
        raise NotImplementedError, NotImplementedMessage

    def msg(self, msg):
        """ used to write to a debugger that is connected to this
        server; `str' written will have a newline added to it
        """
        if hasattr(self.output, 'writeline'):
            self.output.writeline(msg)
        elif hasattr(self.output, 'writelines'):
            self.output.writelines(msg + '\n')

    def msg_nocr(self, msg):
        """ used to write to a debugger that is connected to this
        server; `str' written will not have a newline added to it
        """
        self.output.write(msg)

    def read_command(self, prompt):
        raise NotImplementedError, NotImplementedMessage

    def readline(self, prompt, add_to_history=True):
        raise NotImplementedError, NotImplementedMessage