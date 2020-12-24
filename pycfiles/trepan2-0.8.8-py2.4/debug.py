# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/debug.py
# Compiled at: 2015-05-17 09:17:03
import os, sys, threading
from trepan.processor import complete as Mcomplete
from trepan.processor.command import base_cmd as Mbase_cmd

class DebugCommand(Mbase_cmd.DebuggerCommand):
    """**debug** *python-expression*

Enter a nested debugger that steps through the *python-expression* argument
which is an arbitrary expression to be executed the current
environment."""
    __module__ = __name__
    category = 'support'
    min_args = 1
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = True
    short_help = 'Debug PYTHON-EXPR'
    complete = Mcomplete.complete_identifier

    def run(self, args):
        arg = (' ').join(args[1:])
        curframe = self.proc.curframe
        if not curframe:
            self.msg('No frame selected.')
            return
        for attr in ('prompt_str', 'frame', 'event', 'event_arg', 'curindex'):
            cmd = 'old_%s = self.proc.%s' % (attr, attr)
            exec cmd

        old_lock = self.core.debugger_lock
        old_stop_level = self.core.stop_level
        old_different_line = self.core.stop_level
        self.proc.debug_nest += 1
        self.core.debugger_lock = threading.Lock()
        self.core.stop_level = None
        self.core.different_line = None
        global_vars = curframe.f_globals
        local_vars = curframe.f_locals
        self.section('ENTERING NESTED DEBUGGER')
        self.core.step_ignore = 2
        try:
            ret = sys.call_tracing(eval, (arg, global_vars, local_vars))
            self.msg('R=> %s' % self.proc._saferepr(ret))
        except:
            pass

        self.section('LEAVING NESTED DEBUGGER')
        self.core.debugger_lock = old_lock
        self.core.stop_level = old_stop_level
        self.core.different_line = old_different_line
        self.proc.continue_running = False
        self.proc.debug_nest -= 1
        for attr in ('prompt_str', 'frame', 'event', 'event_arg', 'curindex'):
            cmd = 'self.proc.%s = old_%s' % (attr, attr)
            exec cmd

        if hasattr(self.proc, 'print_location'):
            self.proc.print_location()
        return False


if __name__ == '__main__':
    import inspect
    from trepan.processor import cmdproc as Mcmdproc
    from trepan import debugger
    d = debugger.Debugger()
    cp = d.core.processor
    cp.curframe = inspect.currentframe()
    (cp.stack, cp.curindex) = Mcmdproc.get_stack(cp.curframe, None, None, cp)
    command = DebugCommand(cp)

    def test_fn():
        return 5


    command.run(['debug', 'test_fn()'])