# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/inout/scriptin.py
# Compiled at: 2015-02-16 15:47:50
"""Debugger Script input interface. """
import types
from trepan.inout import base as Mbase

class ScriptInput(Mbase.DebuggerInputBase):
    """Debugger Script input - largely the same as DebuggerInput."""

    def __init__(self, inp, opts=None):
        self.input = None
        self.line_edit = False
        self.name = None
        self.open(inp, opts)
        return

    def close(self):
        if self.input:
            self.input.close()

    def open(self, inp, opts=None):
        """Use this to set what file to read from. """
        if isinstance(inp, types.FileType):
            self.input = inp
        elif isinstance(inp, types.StringType):
            self.name = inp
            self.input = open(inp, 'r')
        else:
            raise IOError('Invalid input type (%s) for %s' % (type(inp),
             inp))

    def readline(self, prompt='', use_raw=None):
        """Read a line of input. Prompt and use_raw exist to be
        compatible with other input routines and are ignored.
        EOFError will be raised on EOF.
        """
        line = self.input.readline()
        if not line:
            raise EOFError
        return line.rstrip('\n')


if __name__ == '__main__':
    import os
    my_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scriptin.py')
    inp = ScriptInput(my_file)
    line = inp.readline()
    print line
    inp.close()
    inp.open(my_file, opts={'use_raw': False})
    while True:
        try:
            inp.readline()
        except EOFError:
            break

    try:
        inp.readline()
    except EOFError:
        print 'EOF handled correctly'