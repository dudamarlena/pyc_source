# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/trace.py
# Compiled at: 2015-02-16 15:47:50
from tracer import EVENT2SHORT
from trepan import vprocessor as Mprocessor

class PrintProcessor(Mprocessor.Processor):
    """ A processor that just prints out events as we see them. This
    is suitable for example for line/call tracing. We assume that the
    caller is going to filter out which events it wants printed or
    whether it wants any printed at all.
    """

    def __init__(self, debugger, opts=None):
        Mprocessor.Processor.__init__(self, debugger)

    def event_processor(self, frame, event, arg):
        """A simple event processor that prints out events."""
        out = self.debugger.intf[(-1)].output
        lineno = frame.f_lineno
        filename = self.core.canonic_filename(frame)
        filename = self.core.filename(filename)
        if not out:
            print '%s - %s:%d' % (event, filename, lineno)
        else:
            out.write('%s - %s:%d' % (event, filename, lineno))
            if arg is not None:
                out.writeline(', %s ' % repr(arg))
            else:
                out.writeline('')
        return self.event_processor