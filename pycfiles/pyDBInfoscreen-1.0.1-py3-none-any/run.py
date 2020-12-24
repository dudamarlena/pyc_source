# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/run.py
# Compiled at: 2013-03-18 19:40:11
import os
from import_relative import import_relative
Mbase_cmd = import_relative('base_cmd', top_name='pydbgr')
Mexcept = import_relative('exception', '...', 'pydbgr')

class RunCommand(Mbase_cmd.DebuggerCommand):
    """run

Soft restart debugger and program via a *DebuggerRestart*
exception."""
    __module__ = __name__
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
    mock = import_relative('mock')
    (d, cp) = mock.dbg_setup()
    command = RunCommand(cp)
    try:
        command.run([])
    except Mexcept.DebuggerRestart:
        import sys
        print 'Got restart exception: parms %s' % sys.exc_value.sys_argv