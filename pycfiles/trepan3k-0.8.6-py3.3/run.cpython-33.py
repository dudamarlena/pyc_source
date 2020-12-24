# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/run.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 1992 bytes
import os
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan import exception as Mexcept

class RunCommand(Mbase_cmd.DebuggerCommand):
    __doc__ = '**run**\n\nSoft restart debugger and program via a *DebuggerRestart*\nexception.\n\nSee also:\n---------\n\n`restart` for another way to restart the debugged program.\n\nSee `quit`, `exit` or `kill` for termination commands.\n'
    aliases = ('R', )
    category = 'support'
    min_args = 0
    max_args = 0
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = '(Soft) restart program via a DebuggerRestart exception'

    def run(self, args):
        confirmed = self.confirm('Soft restart', False)
        if confirmed:
            self.core.step_ignore = 0
            self.core.step_events = None
            raise Mexcept.DebuggerRestart(self.core.debugger.restart_argv())
        return


if __name__ == '__main__':
    from trepan.processor.command import mock
    d, cp = mock.dbg_setup()
    command = RunCommand(cp)
    try:
        command.run([])
    except Mexcept.DebuggerRestart:
        import sys
        print('Got restart exception: parms %s' % sys.exc_info()[1].sys_argv)