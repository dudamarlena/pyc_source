# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/finish.py
# Compiled at: 2013-03-11 21:31:04
import os, sys
from import_relative import import_relative
Mbase_cmd = import_relative('base_cmd', top_name='pydbgr')
Mstack = import_relative('stack', '...lib', 'pydbgr')
Mcmdfns = import_relative('cmdfns', '..', 'pydbgr')

class FinishCommand(Mbase_cmd.DebuggerCommand):
    """**finish** [*level*]

Continue execution until leaving the current function. When *level* is
specified, that many frame levels need to be popped. Note that *yield*
and exceptions raised my reduce the number of stack frames. Also, if a
thread is switched, we stop ignoring levels.

See the `break` command if you want to stop at a particular point in a
program."""
    __module__ = __name__
    category = 'running'
    execution_set = ['Running']
    min_args = 0
    max_args = 1
    name = os.path.basename(__file__).split('.')[0]
    need_stack = True
    short_help = 'Execute until selected stack frame returns'

    def run(self, args):
        if self.proc.stack is None:
            return False
        if len(args) <= 1:
            levels = 1
        else:
            max_levels = len(self.proc.stack)
            levels = self.proc.get_int(args[1], default=1, cmdname='finish')
            if levels is None:
                return False
        self.core.step_events = [
         'return']
        self.core.stop_on_finish = True
        self.core.stop_level = Mstack.count_frames(self.proc.frame) - levels
        self.core.last_frame = self.proc.frame
        self.proc.continue_running = True
        return True


if __name__ == '__main__':
    from mock import MockDebugger
    d = MockDebugger()
    cmd = FinishCommand(d.core.processor)

    def demo_finish(cmd):
        for c in (['finish', '1'], ['finish', 'wrong', 'number', 'of', 'args'], ['finish', '5'], ['finish', '0*5+1']):
            cmd.continue_running = False
            cmd.proc.stack = [(sys._getframe(0), 14)]
            result = cmd.run(c)
            print 'Execute result: %s' % result
            print 'stop_frame %s, continue_running: %s' % (cmd.core.stop_frame, cmd.continue_running)


    demo_finish(cmd)