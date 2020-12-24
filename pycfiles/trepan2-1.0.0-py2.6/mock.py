# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/mock.py
# Compiled at: 2017-10-27 23:34:05
""" Not a command. A stub class used by a command in its 'main' for
demonstrating how the command works."""
import sys
from trepan.lib import breakpoint, default

class MockIO:

    def readline(self, prompt='', add_to_history=False):
        print prompt
        return 'quit'

    def output(self):
        print


class MockUserInterface:

    def __init__(self):
        self.io = MockIO()
        self.output = MockIO()

    def confirm(self, msg, default):
        print '** %s' % msg
        return True

    def errmsg(self, msg):
        print '** %s' % msg

    def finalize(self, last_wishes=None):
        pass

    def msg(self, msg):
        print msg

    def msg_nocr(self, msg):
        sys.stdout.write(msg)


class MockProcessor:

    def __init__(self, core):
        self.core = core
        self.debugger = core.debugger
        self.continue_running = False
        self.curframe = None
        self.event2short = {}
        self.frame = None
        self.intf = core.debugger.intf
        self.last_command = None
        self.stack = []
        return

    def get_int(self, arg, min_value=0, default=1, cmdname=None, at_most=None):
        return

    def undefined_cmd(self, cmd):
        self.intf[(-1)].errmsg('Undefined mock command: "%s' % cmd)


import tracefilter

class MockDebuggerCore:

    def __init__(self, debugger):
        self.debugger = debugger
        self.execution_status = 'Pre-execution'
        self.filename_cache = {}
        self.ignore_filter = tracefilter.TraceFilter([])
        self.bpmgr = breakpoint.BreakpointManager()
        self.processor = MockProcessor(self)
        self.step_ignore = -1
        self.stop_frame = None
        self.last_lineno = None
        self.last_offset = None
        self.last_filename = None
        self.different_line = None
        self.from_ipython = False
        return

    def set_next(self, frame, step_events=None):
        pass

    def stop(self):
        pass

    def canonic(self, filename):
        return filename

    def canonic_filename(self, frame):
        return frame.f_code.co_filename

    def filename(self, name):
        return name

    def is_running(self):
        return 'Running' == self.execution_status

    def get_file_breaks(self, filename):
        return []


class MockDebugger:

    def __init__(self):
        self.intf = [
         MockUserInterface()]
        self.core = MockDebuggerCore(self)
        self.settings = default.DEBUGGER_SETTINGS
        self.from_ipython = False
        self.orig_sys_argv = None
        self.program_sys_argv = []
        return

    def stop(self):
        pass

    def restart_argv(self):
        return []


def dbg_setup(d=None):
    if d is None:
        d = MockDebugger()
    from trepan.processor import cmdproc
    cp = cmdproc.CommandProcessor(d.core)
    return (d, cp)