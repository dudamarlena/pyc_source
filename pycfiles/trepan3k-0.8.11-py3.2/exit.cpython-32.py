# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/exit.py
# Compiled at: 2015-10-12 15:50:30
import os
from trepan.processor.command import base_cmd as Mbase_cmd

class ExitCommand(Mbase_cmd.DebuggerCommand):
    """**exit** [*exitcode*]

Hard exit of the debugged program.

The program being debugged is exited via *sys.exit()*. If a return code
is given, that is the return code passed to *sys.exit()*, the
return code that will be passed back to the OS.

See also:
---------

See `quit` and `kill`.
"""
    category = 'support'
    min_args = 0
    max_args = 1
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Exit program via sys.exit()'

    def run(self, args):
        self.core.stop()
        self.core.execution_status = 'Exit command'
        if len(args) <= 1:
            exit_code = 0
        else:
            exit_code = self.proc.get_int(args[1], default=0, cmdname='exit')
        if exit_code is None:
            return False
        else:
            import sys
            sys.exit(int(exit_code))
            return True


if __name__ == '__main__':
    from trepan.processor.command import mock
    d, cp = mock.dbg_setup()
    command = ExitCommand(cp)
    command.run(['exit', 'wrong', 'number', 'of', 'args'])
    command.run(['exit', 'foo'])
    command.run(['exit', '10'])