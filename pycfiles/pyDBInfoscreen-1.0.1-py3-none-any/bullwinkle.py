# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/interfaces/bullwinkle.py
# Compiled at: 2013-03-22 03:41:35
__doc__ = 'Interface when communicating with the user in the same process as\n    the debugged program.'
import atexit, pprint
from import_relative import *
import_relative('interfaces', '..', 'pydbgr')
Minterface = import_relative('interface', '..', 'pydbgr')
Minput = import_relative('input', '..io', 'pydbgr')
Moutput = import_relative('output', '..io', 'pydbgr')

class BWInterface(Minterface.DebuggerInterface):
    """Interface when communicating with the user in the same
    process as the debugged program."""
    __module__ = __name__

    def __init__(self, inp=None, out=None, opts=None):
        atexit.register(self.finalize)
        self.input = inp or Minput.DebuggerUserInput()
        self.output = out or Moutput.DebuggerUserOutput()
        self.pp = pprint.PrettyPrinter()

    def close(self):
        """ Closes both input and output """
        self.input.close()
        self.output.close()

    def errmsg(self, msg):
        """Common routine for reporting debugger error messages.
           """
        return self.msg(msg)

    def finalize(self, last_wishes=None):
        self.close()

    def msg(self, msg):
        self.output.write(self.pp.pformat(msg) + '\n')

    def read_command(self):
        line = self.readline('Bullwinkle read: ')
        try:
            command = eval(line)
        except:
            return 'eval error'

        return command

    def readline(self, prompt=''):
        return self.input.readline(prompt=prompt)


if __name__ == '__main__':
    intf = BWInterface()
    intf.msg('Testing1, 2, 3')
    import sys
    if len(sys.argv) > 1:
        try:
            entry = intf.read_command()
        except EOFError:
            print 'No input EOF: '
        else:
            intf.msg(entry)