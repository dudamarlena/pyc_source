# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/inout/input.py
# Compiled at: 2017-08-12 23:13:24
"""Debugger input possibly attached to a user or interactive. """
import sys, types, StringIO
from trepan import misc as Mmisc
from trepan.inout import base as Mbase

def readline_importable():
    try:
        import readline
        return True
    except ImportError:
        return False


class DebuggerUserInput(Mbase.DebuggerInputBase):
    """Debugger input connected to what we think of as a end-user input
    as opposed to a relay mechanism to another process. Input could be
    interative terminal, but it might be file input."""
    __module__ = __name__

    def __init__(self, inp=None, opts=None):
        self.input = inp or sys.stdin
        self.line_edit = None
        self.open(self.input, opts)
        return

    def close(self):
        self.input.close()
        self.closed = True

    DEFAULT_OPEN_READ_OPTS = {'use_raw': True, 'try_readline': True}

    def use_history(self):
        return self.use_raw and readline_importable()

    def open(self, inp, opts={}):
        """Use this to set where to read from.

        Set opts['try_lineedit'] if you want this input to interact
        with GNU-like readline library. By default, we will assume to
        try importing and using readline. If readline is not
        importable, line editing is not available whether or not
        opts['try_readline'] is set.

        Set opts['use_raw'] if input should use Python's use_raw(). If
        however 'inp' is a string and opts['use_raw'] is not set, we
        will assume no raw output. Note that an individual readline
        may override the setting.
        """
        get_option = lambda key: Mmisc.option_set(opts, key, self.DEFAULT_OPEN_READ_OPTS)
        if isinstance(inp, types.FileType) or isinstance(inp, StringIO.StringIO) or hasattr(inp, 'isatty') and inp.isatty():
            self.use_raw = get_option('use_raw')
        elif isinstance(inp, types.StringType):
            if opts is None:
                self.use_raw = False
            else:
                self.use_raw = get_option('use_raw')
            inp = open(inp, 'r')
        else:
            raise IOError('Invalid input type (%s) for %s' % (type(inp), inp))
        self.input = inp
        self.line_edit = get_option('try_readline') and readline_importable()
        self.closed = False
        return

    def readline(self, use_raw=None, prompt=''):
        """Read a line of input. EOFError will be raised on EOF.

        Note: some user interfaces may decide to arrange to call
        DebuggerOutput.write() first with the prompt rather than pass
        it here.. If `use_raw' is set raw_input() will be used in that
        is supported by the specific input input. If this option is
        left None as is normally expected the value from the class
        initialization is used.
        """
        if use_raw is None:
            use_raw = self.use_raw
        if use_raw:
            try:
                return raw_input(prompt)
            except ValueError:
                raise EOFError

        else:
            line = self.input.readline()
            if not line:
                raise EOFError
            return line.rstrip('\n')
        return


if __name__ == '__main__':
    print 'readline importable: ', readline_importable()
    inp = DebuggerUserInput('input.py')
    line = inp.readline()
    print line
    inp.close()
    inp.open('input.py', opts={'use_raw': False})
    while True:
        try:
            inp.readline()
        except EOFError:
            break

    try:
        inp.readline()
    except EOFError:
        print 'EOF handled correctly'
    else:
        if len(sys.argv) > 1:
            inp = DebuggerUserInput()
            try:
                print 'Type some characters:',
                line = inp.readline()
                print 'You typed: %s' % line
                print 'Type some more characters (raw):',
                line = inp.readline(True)
                print 'Type even more characters (not raw):',
                line = inp.readline(True)
                print 'You also typed: %s' % line
            except EOFError:
                print 'Got EOF'