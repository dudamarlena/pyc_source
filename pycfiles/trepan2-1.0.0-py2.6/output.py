# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/inout/output.py
# Compiled at: 2015-06-01 11:58:30
"""Debugger output. """
import types, sys, StringIO
from trepan.inout import base as Mbase

class DebuggerUserOutput(Mbase.DebuggerOutputBase):
    """Debugger output shown directly to what we think of as end-user
    ouptut as opposed to a relay mechanism to another process. Output
    could be an interactive terminal, but it might also be file output"""

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
            raise IOError('Invalid output type (%s) for %s' % (type(output),
             output))
        self.output = output
        self.closed = False

    def write(self, msg):
        """ This method the debugger uses to write. In contrast to
        writeline, no newline is added to the end to `str'.
        """
        if hasattr(self.output, 'closed') and self.output.closed:
            raise IOError('writing %s on a closed file' % msg)
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