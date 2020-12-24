# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/next.py
# Compiled at: 2015-06-03 13:30:53
import os
from trepan.processor.command import base_cmd
from trepan.processor import cmdfns as Mcmdfns

class NextCommand(base_cmd.DebuggerCommand):
    aliases = ('next+', 'next-', 'n', 'n-', 'n+')
    category = 'running'
    execution_set = ['Running']
    min_args = 0
    max_args = 1
    name = os.path.basename(__file__).split('.')[0]
    need_stack = True
    short_help = 'Step program without entering called functions'

    def run(self, args):
        """**next**[**+**|**-**] [*count*]

Step one statement ignoring steps into function calls at this level.

With an integer argument, perform `next` that many times. However if
an exception occurs at this level, or we *return*, *yield* or the
thread changes, we stop regardless of count.

A suffix of `+` on the command or an alias to the command forces to
move to another line, while a suffix of `-` does the opposite and
disables the requiring a move to a new line. If no suffix is given,
the debugger setting 'different-line' determines this behavior.

See also:
---------

`step`, `skip`, `jump` (there's no `hop` yet), `continue`, and
`finish` for other ways to progress execution.
"""
        if len(args) <= 1:
            step_ignore = 0
        else:
            step_ignore = self.proc.get_int(args[1], default=1, cmdname='next')
            if step_ignore is None:
                return False
            step_ignore -= 1
        self.core.different_line = Mcmdfns.want_different_line(args[0], self.debugger.settings['different'])
        self.core.set_next(self.proc.frame, step_ignore)
        self.proc.continue_running = True
        return True


if __name__ == '__main__':
    from mock import MockDebugger
    d = MockDebugger()
    cmd = NextCommand(d.core.processor)
    for c in (['n', '5'],
     [
      'next', '1+2'],
     [
      'n', 'foo']):
        d.core.step_ignore = 0
        cmd.continue_running = False
        result = cmd.run(c)
        print('Run result: %s' % result)
        print('step_ignore %d, continue_running: %s' % (d.core.step_ignore,
         cmd.continue_running))

    for c in (['n'], ['next+'], ['n-']):
        d.core.step_ignore = 0
        cmd.continue_running = False
        result = cmd.run(c)
        print(cmd.core.different_line)