# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/inout/fifoclient.py
# Compiled at: 2015-05-13 15:30:36
"""Debugger FIFO Input/Output interface. """
import tempfile, os
from trepan.lib import default as Mdefault, file as Mfile
from trepan import misc as Mmisc
from trepan.inout.base import DebuggerInOutBase

class FIFOClient(DebuggerInOutBase):
    """Debugger Client Input/Output Socket."""
    __module__ = __name__
    DEFAULT_INIT_OPTS = {'open': True}

    def __init__(self, inp=None, opts=None):
        get_option = lambda key: Mmisc.option_set(opts, key, Mdefault.CLIENT_SOCKET_OPTS)
        self.state = 'disconnected'
        self.flush_after_write = True
        self.input = None
        self.output = None
        self.line_edit = False
        self.state = 'disconnected'
        open_pid = get_option('open')
        if open_pid:
            self.open(open_pid)
        return

    def close(self):
        """ Closes both input and output """
        self.state = 'closing'
        if self.input:
            self.input.close()
        if self.output:
            self.output.close()
        self.state = 'disconnnected'
        self.closed = True

    def flush(self):
        return self.output.flush()

    def open(self, pid, opts=None):
        d = tempfile.gettempdir()
        self.out_name = os.path.join(d, 'trepan-%s.in' % pid)
        self.in_name = os.path.join(d, 'trepan-%s.out' % pid)
        is_readable = Mfile.readable(self.out_name)
        if not is_readable:
            if is_readable is None:
                raise IOError("output FIFO %s doesn't exist" % self.out_name)
            else:
                raise IOError('output FIFO %s is not readable' % self.out_name)
        is_readable = Mfile.readable(self.in_name)
        if not is_readable:
            if is_readable is None:
                raise IOError("input FIFO %s doesn't exist" % self.in_name)
            else:
                raise IOError('output FIFO %s is not readable' % self.out_name)
            self.state = 'active'
        self.closed = False
        return

    def read_msg(self):
        """Read a line of input. EOFError will be raised on EOF.

        Note that we don't support prompting"""
        if self.state == 'active':
            if not self.input:
                self.input = open(self.in_name, 'r')
            line = self.input.readline()
            if not line:
                self.state = 'disconnected'
                raise EOFError
            return line.encode('utf-8')
        else:
            raise IOError('readline called in state: %s.' % self.state)

    def write(self, msg):
        """ This method the debugger uses to write. In contrast to
        writeline, no newline is added to the end to `str'.
        """
        if self.state == 'active':
            if not self.output:
                self.output = open(self.out_name, 'w')
        else:
            raise EOFError
        self.output.write(msg)
        if self.flush_after_write:
            self.flush()


if __name__ == '__main__':
    fifo = FIFOClient(opts={'open': False})
    import sys
    if len(sys.argv) > 1:
        print ('Connecting...', )
        fifo.open(sys.argv[1])
        print 'connected.'
        while True:
            prompt = fifo.readline()
            line = raw_input(prompt)
            if len(line) == 0:
                break
            try:
                line = fifo.writeline(line)
                print ('Got: ', fifo.readline())
            except EOFError:
                break

    fifo.close()