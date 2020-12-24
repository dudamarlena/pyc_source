# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/inout/base.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 5359 bytes
"""classes to support communication to and from the debugger.  This
communcation might be to/from another process or another computer.
And reading may be from a debugger command script.

For example, we'd like to support Sockets, and serial lines and file
reading, as well a readline-type input. Encryption and Authentication
methods might decorate some of the communication channels.

Some ideas originiated as part of Matt Fleming's 2006 Google Summer of
Code project.
"""
from abc import ABCMeta
NotImplementedMessage = 'This method must be overriden in a subclass'

class DebuggerInputBase(metaclass=ABCMeta):
    __doc__ = 'This is an abstract class that specifies debugger input.'

    def __init__(self, inp=None, opts=None):
        self.input = None
        return

    def close(self):
        if self.input:
            self.input.close()

    def use_history(self):
        return False

    def open(self, inp, opts=None):
        """Use this to set where to read from. """
        raise NotImplementedError(NotImplementedMessage)

    def readline(self, use_raw=None):
        """Read a line of input. EOFError will be raised on EOF.

        Note that we don't support prompting first. Instead, arrange
        to call DebuggerOutput.write() first with the prompt. If
        `use_raw' is set raw_input() will be used in that is supported
        by the specific input input. If this option is left None as is
        normally expected the value from the class initialization is
        used.
        """
        raise NotImplementedError(NotImplementedMessage)


class DebuggerInOutBase(metaclass=ABCMeta):
    __doc__ = ' This is an abstract class that specifies debugger output. '

    def __init__(self, out=None, opts=None):
        self.output = None
        return

    def close(self):
        if self.output:
            self.output.close()

    def flush(self):
        raise NotImplementedError(NotImplementedMessage)

    def write(self, output):
        """Use this to set where to write to. output can be a
        file object or a string. This code raises IOError on error.
        """
        raise NotImplementedError(NotImplementedMessage)

    def writeline(self, msg):
        """ used to write to a debugger that is connected to this
        server; `str' written will have a newline added to it
        """
        self.write('%s\n' % msg)


class TrepanInOutBase(metaclass=ABCMeta):
    __doc__ = ' This is an abstract class that specifies debugger input output when\n    handled by the same channel, e.g. a socket or tty.\n    '

    def __init__(self, inout=None, opts=None):
        self.inout = None
        return

    def close(self):
        if self.inout:
            self.inout.close()

    def flush(self):
        raise NotImplementedError(NotImplementedMessage)

    def open(self, inp, opts=None):
        """Use this to set where to read from. """
        raise NotImplementedError(NotImplementedMessage)

    def readline(self, use_raw=None):
        """Read a line of input. EOFError will be raised on EOF.

        Note that we don't support prompting first. Instead, arrange
        to call DebuggerOutput.write() first with the prompt. If
        `use_raw' is set raw_input() will be used in that is supported
        by the specific input input. If this option is left None as is
        normally expected the value from the class initialization is
        used.
        """
        raise NotImplementedError(NotImplementedMessage)

    def write(self, output):
        """Use this to set where to write to. output can be a
        file object or a string. This code raises IOError on error.
        """
        raise NotImplementedError(NotImplementedMessage)

    def writeline(self, msg):
        """ used to write to a debugger that is connected to this
        server; `str' written will have a newline added to it
        """
        self.write('%s\n' % msg)


if __name__ == '__main__':

    class MyInput(DebuggerInputBase):

        def open(self, inp, opts=None):
            print('open(%s) called' % inp)


    class MyOutput(DebuggerInOutBase):

        def writeline(self, s):
            print('writeline:', s)


    inp = MyInput()
    inp.open('foo')
    inp.close()
    out = MyOutput()
    out.writeline('foo')
    try:
        out.write('foo')
    except NotImplementedError:
        print('Ooops. Forgot to implement write()')