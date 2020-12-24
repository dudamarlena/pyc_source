# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/io/base_io.py
# Compiled at: 2013-01-04 05:13:40
__doc__ = "classes to support communication to and from the debugger.  This\ncommuncation might be to/from another process or another computer.\nAnd reading may be from a debugger command script.\n\nFor example, we'd like to support Sockets, and serial lines and file\nreading, as well a readline-type input. Encryption and Authentication\nmethods might decorate some of the communication channels.\n\nSome ideas originiated as part of Matt Fleming's 2006 Google Summer of\nCode project.\n"
NotImplementedMessage = 'This method must be overriden in a subclass'

class DebuggerInputBase(object):
    """ This is an abstract class that specifies debugger input. """
    __module__ = __name__

    def __init__(self, inp=None, opts=None):
        self.input = None
        return

    def close(self):
        if self.input:
            self.input.close()

    def open(self, inp, opts=None):
        """Use this to set where to read from. """
        raise NotImplementedError, NotImplementedMessage

    def readline(self, use_raw=None):
        """Read a line of input. EOFError will be raised on EOF.  

        Note that we don't support prompting first. Instead, arrange
        to call DebuggerOutput.write() first with the prompt. If
        `use_raw' is set raw_input() will be used in that is supported
        by the specific input input. If this option is left None as is
        normally expected the value from the class initialization is
        used.
        """
        raise NotImplementedError, NotImplementedMessage


class DebuggerOutputBase(object):
    """ This is an abstract class that specifies debugger output. """
    __module__ = __name__

    def __init__(self, out=None, opts=None):
        self.output = None
        return

    def close(self):
        if self.output:
            self.output.close()

    def flush(self):
        raise NotImplementedError, NotImplementedMessage

    def write(self, output):
        """Use this to set where to write to. output can be a 
        file object or a string. This code raises IOError on error.
        """
        raise NotImplementedError, NotImplementedMessage

    def writeline(self, msg):
        """ used to write to a debugger that is connected to this
        server; `str' written will have a newline added to it
        """
        self.write('%s\n' % msg)


class DebuggerInOutBase(object):
    """ This is an abstract class that specifies debugger input output when
    handled by the same channel, e.g. a socket or tty.
    """
    __module__ = __name__

    def __init__(self, inout=None, opts=None):
        self.inout = None
        return

    def close(self):
        if self.inout:
            self.inout.close()

    def flush(self):
        raise NotImplementedError, NotImplementedMessage

    def open(self, inp, opts=None):
        """Use this to set where to read from. """
        raise NotImplementedError, NotImplementedMessage

    def readline(self, use_raw=None):
        """Read a line of input. EOFError will be raised on EOF.  

        Note that we don't support prompting first. Instead, arrange
        to call DebuggerOutput.write() first with the prompt. If
        `use_raw' is set raw_input() will be used in that is supported
        by the specific input input. If this option is left None as is
        normally expected the value from the class initialization is
        used.
        """
        raise NotImplementedError, NotImplementedMessage

    def write(self, output):
        """Use this to set where to write to. output can be a 
        file object or a string. This code raises IOError on error.
        """
        raise NotImplementedError, NotImplementedMessage

    def writeline(self, msg):
        """ used to write to a debugger that is connected to this
        server; `str' written will have a newline added to it
        """
        self.write('%s\n' % msg)


if __name__ == '__main__':

    class MyInput(DebuggerInputBase):
        __module__ = __name__

        def open(self, inp, opts=None):
            print 'open(%s) called' % inp


    class MyOutput(DebuggerOutputBase):
        __module__ = __name__

        def writeline(self, s):
            print 'writeline:', s


    inp = MyInput()
    inp.open('foo')
    inp.close()
    out = MyOutput()
    out.writeline('foo')
    try:
        out.write('foo')
    except NotImplementedError:
        print 'Ooops. Forgot to implement write()'