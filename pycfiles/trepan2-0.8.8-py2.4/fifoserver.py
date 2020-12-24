# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/inout/fifoserver.py
# Compiled at: 2015-02-16 15:47:50
"""Debugger FIFO Input/Output interface. """
import os
if hasattr(os, 'mkfifo'):
    import atexit, tempfile
    from trepan import misc as Mmisc
    from trepan.inout.base import DebuggerInOutBase

    class FIFOServer(DebuggerInOutBase):
        """Debugger Server Input/Output Socket."""
        __module__ = __name__
        DEFAULT_INIT_OPTS = {'open': True}

        def __init__(self, opts=None):
            get_option = lambda key: Mmisc.option_set(opts, key, self.DEFAULT_INIT_OPTS)
            atexit.register(self.close)
            self.flush_after_write = True
            self.line_edit = False
            self.in_name = None
            self.input = None
            self.out_name = None
            self.output = None
            self.state = 'disconnected'
            if get_option('open'):
                self.open(opts)
            return

        def close(self):
            """ Closes both input and output. """
            self.state = 'closing'
            if self.input:
                self.input.close()
            if self.in_name and os.path.exists(self.in_name):
                os.unlink(self.in_name)
            if self.output:
                self.output.close()
            if self.out_name and os.path.exists(self.out_name):
                os.unlink(self.out_name)
            self.state = 'disconnnected'

        def flush(self):
            return self.output.flush()

        def open(self, opts=None):
            d = tempfile.gettempdir()
            pid = os.getpid()
            self.out_name = os.path.join(d, 'trepan-%s.out' % pid)
            self.in_name = os.path.join(d, 'trepan-%s.in' % pid)
            try:
                os.mkfifo(self.in_name)
                os.mkfifo(self.out_name)
                self.state = 'active'
            except OSError:
                self.state = 'error'

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
                return line.rstrip('\n')
            else:
                raise EOFError

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
        fifo = FIFOServer(opts={'open': False})
        import sys
        if len(sys.argv) > 1:
            fifo.open()
            print 'Looking for input on %s"...' % fifo.in_name
            while True:
                try:
                    fifo.write('nu?')
                    fifo.writeline(' ')
                    line = fifo.readline()
                    print line
                    fifo.writeline('ack: ' + line)
                except EOFError:
                    break

        fifo.close()