# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/io/scriptin.py
# Compiled at: 2013-03-23 12:46:43
__doc__ = 'Debugger Script input interface. '
import types
from import_relative import import_relative, get_srcdir
Mbase_io = import_relative('base_io', top_name='pydbgr')

class ScriptInput(Mbase_io.DebuggerInputBase):
    """Debugger Script input - largely the same as DebuggerInput."""
    __module__ = __name__

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
            raise IOError, 'Invalid input type (%s) for %s' % (type(inp), inp)

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
    inp = ScriptInput('scriptin.py')
    line = inp.readline()
    print line
    inp.close()
    import os
    my_file = os.path.join(get_srcdir(), 'scriptin.py')
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