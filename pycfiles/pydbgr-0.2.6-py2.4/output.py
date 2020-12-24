# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/io/output.py
# Compiled at: 2013-03-23 12:47:32
"""Debugger output. """
import types, sys, StringIO
from import_relative import import_relative
Mbase_io = import_relative('base_io', top_name='pydbgr')

class DebuggerUserOutput(Mbase_io.DebuggerOutputBase):
    """Debugger output shown directly to what we think of as end-user
    ouptut as opposed to a relay mechanism to another process. Output
    could be an interactive terminal, but it might also be file output"""
    __module__ = __name__

    def __init__(self, out=None, opts=None):
        self.flush_after_write = False
        self.output = out or sys.stdout
        self.open(self.output, opts)

    def flush(self):
        return self.output.flush()

    def open(self, output, opts=None):
        """Use this to set where to write to. output can be a 
        file object or a string. This code raises IOError on error."""
        if isinstance(output, types.FileType) or isinstance(output, StringIO.StringIO) or output == sys.stdout:
            pass
        elif isinstance(output, types.StringType):
            output = open(output, 'w')
        else:
            raise IOError, 'Invalid output type (%s) for %s' % (type(output), output)
        self.output = output

    def write(self, msg):
        """ This method the debugger uses to write. In contrast to
        writeline, no newline is added to the end to `str'.
        """
        self.output.write(msg)
        if self.flush_after_write:
            self.flush()


if __name__ == '__main__':
    out = DebuggerUserOutput()
    out.writeline('Hello, world!')
    out.write('Hello')
    out.writeline(', again.')
    out.open(sys.stdout)
    out.flush_after_write = True
    out.write('Last hello')
    out.close()
    try:
        out.writeline("You won't see me")
    except ValueError:
        pass
    else:
        out.close()