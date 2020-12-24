# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/interfaces/user.py
# Compiled at: 2013-03-17 12:06:19
__doc__ = 'Interface when communicating with the user in the same process as\n    the debugged program.'
import atexit
from import_relative import *
Minterface = import_relative('interface', '...pydbgr')
Minput = import_relative('input', '..io')
Moutput = import_relative('output', '..io')

class UserInterface(Minterface.DebuggerInterface):
    """Interface when communicating with the user in the same
    process as the debugged program."""
    __module__ = __name__
    FILE_HISTORY = '.pydbgr_hist'

    def __init__(self, inp=None, out=None, opts=None):
        atexit.register(self.finalize)
        self.interactive = True
        self.input = inp or Minput.DebuggerUserInput()
        self.output = out or Moutput.DebuggerUserOutput()

    def close(self):
        """ Closes both input and output """
        self.input.close()
        self.output.close()

    def confirm(self, prompt, default):
        """ Called when a dangerous action is about to be done, to make
        sure it's okay. Expect a yes/no answer to `prompt' which is printed,
        suffixed with a question mark and the default value.  The user
        response converted to a boolean is returned."""
        if default:
            prompt += '? (Y or n) '
        else:
            prompt += '? (N or y) '
        while True:
            try:
                reply = self.readline(prompt)
                reply = reply.strip().lower()
            except EOFError:
                return default

            if reply in ('y', 'yes'):
                return True
            elif reply in ('n', 'no'):
                return False
            else:
                self.msg('Please answer y or n.')

        return default

    def errmsg(self, msg, prefix='** '):
        """Common routine for reporting debugger error messages.
           """
        return self.msg('%s%s' % (prefix, msg))

    def finalize(self, last_wishes=None):
        self.close()

    def read_command(self, prompt=''):
        line = self.readline(prompt)
        return line

    def readline(self, prompt=''):
        if hasattr(self.input, 'use_raw') and not self.input.use_raw and prompt and len(prompt) > 0:
            self.output.write(prompt)
            self.output.flush()
        return self.input.readline(prompt=prompt)


if __name__ == '__main__':
    intf = UserInterface()
    intf.errmsg('Houston, we have a problem here!')
    import sys
    if len(sys.argv) > 1:
        try:
            line = intf.readline('Type something: ')
        except EOFError:
            print 'No input EOF: '
        else:
            print 'You typed: %s' % line

        line = intf.confirm('Are you sure', False)
        print 'You typed: %s' % line
        line = intf.confirm('Are you not sure', True)
        print 'You typed: %s' % line