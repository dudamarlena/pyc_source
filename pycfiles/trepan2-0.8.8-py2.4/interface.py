# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/interface.py
# Compiled at: 2014-10-24 20:18:27
"""A base class for a debugger interface."""
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
        raise NotImplementedError(NotImplementedMessage)

    def confirm(self, prompt, default):
        """ Called when a dangerous action is about to be done to make sure
        it's okay. `prompt' is printed; user response is returned."""
        raise NotImplementedError(NotImplementedMessage)

    def errmsg(self, str, prefix='** '):
        """Common routine for reporting debugger error messages.
           """
        raise NotImplementedError(NotImplementedMessage)

    def finalize(self, last_wishes=None):
        raise NotImplementedError(NotImplementedMessage)

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
        raise NotImplementedError(NotImplementedMessage)

    def readline(self, prompt, add_to_history=True):
        raise NotImplementedError(NotImplementedMessage)