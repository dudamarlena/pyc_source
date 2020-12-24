# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/restart.py
# Compiled at: 2013-01-12 04:25:15
import atexit, os
from import_relative import import_relative
Mdebugger = import_relative('debugger', '...', 'pydbgr')
Mbase_cmd = import_relative('base_cmd', top_name='pydbgr')
Mcomcodes = import_relative('comcodes', '...interfaces', 'pydbgr')
debugger = import_relative('debugger', '...')
Mmisc = import_relative('misc', '...', 'pydbgr')

class RestartCommand(Mbase_cmd.DebuggerCommand):
    """**restart**

Restart debugger and program via an *exec()* call. All state is lost,
and new copy of the debugger is used."""
    __module__ = __name__
    category = 'support'
    min_args = 0
    max_args = 0
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = '(Hard) restart of program via execv()'

    def run(self, args):
        sys_argv = self.debugger.restart_argv()
        if sys_argv and len(sys_argv) > 0:
            confirmed = self.confirm('Restart (execv)', False)
            if confirmed:
                self.msg(Mmisc.wrapped_lines("Re exec'ing:", repr(sys_argv), self.settings['width']))
                try:
                    atexit._run_exitfuncs()
                except:
                    pass
                else:
                    os.execvp(sys_argv[0], sys_argv)
        else:
            self.errmsg('No executable file and command options recorded.')


if __name__ == '__main__':
    mock = import_relative('mock')
    (d, cp) = mock.dbg_setup()
    command = RestartCommand(cp)
    command.run([])
    import sys
    if len(sys.argv) > 1:
        d.orig_sys_argv = ['python', sys.argv[0]]
        command.run([])