# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/exit.py
# Compiled at: 2013-01-11 18:05:09
import os
from import_relative import import_relative
Mbase_cmd = import_relative('base_cmd', top_name='pydbgr')
Mcmdfns = import_relative('cmdfns', '..', 'pydbgr')

class ExitCommand(Mbase_cmd.DebuggerCommand):
    """**exit** [*exitcode*]

Hard exit of the debugged program.  

The program being debugged is exited via *sys.exit()*. If a return code
is given, that is the return code passed to *sys.exit()*, the
return code that will be passed back to the OS."""
    __module__ = __name__
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
        import sys
        sys.exit(exit_code)
        return True


if __name__ == '__main__':
    mock = import_relative('mock')
    (d, cp) = mock.dbg_setup()
    command = ExitCommand(cp)
    command.run(['exit', 'wrong', 'number', 'of', 'args'])
    command.run(['exit', 'foo'])
    command.run(['exit', '10'])