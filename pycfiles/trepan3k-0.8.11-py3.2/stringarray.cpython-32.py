# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/inout/stringarray.py
# Compiled at: 2015-04-05 10:01:28
"""Simulate I/O using lists of strings. """
import types
from trepan.inout import base as Mbase

class StringArrayInput(Mbase.DebuggerInputBase):
    """Simulate I/O using an array of strings. Sort of like StringIO, but
    even simplier. """

    def __init__(self, inp=[], opts=None):
        self.input = inp
        self.closed = False

    def close(self):
        """Interface is for compatibility"""
        self.closed = True

    def open(self, inp, opts=None):
        """Use this to set where to read from.
        """
        if isinstance(inp, list):
            self.input = inp
        else:
            raise IOError('Invalid input type (%s) for %s' % (type(inp), inp))

    def readline(self, use_raw=None, prompt=''):
        """Read a line of input. EOFError will be raised on EOF.

        Note that we don't support prompting"""
        if self.closed:
            raise ValueError
        if 0 == len(self.input):
            self.closed = True
            raise EOFError
        line = self.input[0]
        del self.input[0]
        return line


class StringArrayOutput(Mbase.DebuggerInOutBase):
    """Simulate I/O using an array of strings. Sort of like StringIO, but
    even simplier. """

    def __init__(self, out=[], opts=None):
        self.flush_after_write = False
        self.closed = False
        self.output = out

    def close(self):
        """Nothing to do here. Interface is for compatibility"""
        self.closed = True

    def flush(self):
        """Nothing to do here. Interface is for compatibility"""
        pass

    def open(self, output):
        """Use this to set where to write to. output can be a
        file object or a string. This code raises IOError on error.

        If another file was previously open upon calling this open,
        that will be stacked and will come back into use after
        a close_write().
        """
        if isinstance(output, types.Listype):
            self.output = output
        else:
            raise IOError('Invalid output type (%s) for %s' % (type(output),
             output))

    def write(self, msg):
        """ This method the debugger uses to write. In contrast to
        writeline, no newline is added to the end to `str'.
        """
        if self.closed:
            raise ValueError
        if [] == self.output:
            self.output = [
             msg]
        else:
            self.output[(-1)] += msg

    def writeline(self, msg):
        """ used to write to a debugger that is connected to this
        server; Here, we use the null string '' as an indicator of a
        newline.
        """
        self.write(msg)
        self.output.append('')


if __name__ == '__main__':
    inp = StringArrayInput(['Now is the time', 'for all good men'])
    line = inp.readline()
    print(line)
    line = inp.readline()
    print(line)
    try:
        line = inp.readline()
    except EOFError:
        print('EOF hit on read')

    out = StringArrayOutput()
    print(out.output)
    out.writeline('Hello, world!')
    print(out.output)
    out.write('Hello')
    print(out.output)
    out.writeline(', again.')
    print(out.output)
    out.flush_after_write = True
    out.write('Last hello')
    out.close()
    print(out.output)
    try:
        out.writeline("You won't see me")
    except:
        pass

    out.close()
    inp.close()