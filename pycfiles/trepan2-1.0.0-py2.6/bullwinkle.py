# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/interfaces/bullwinkle.py
# Compiled at: 2015-02-16 15:47:50
"""Interface when communicating with the user in the same process as
    the debugged program."""
import atexit, pprint
from trepan import interface as Minterface
from trepan.inout import input as Minput, output as Moutput

class BWInterface(Minterface.DebuggerInterface):
    """Interface when communicating with the user in the same
    process as the debugged program."""

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