# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/restart.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 2589 bytes
import atexit, os
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan import misc as Mmisc

class RestartCommand(Mbase_cmd.DebuggerCommand):
    __doc__ = '**restart**\n\nRestart debugger and program via an *exec()* call. All state is lost,\nand new copy of the debugger is used.\n\nSee also:\n---------\n\n`run` for another way to restart the debugged program.\n\nSee `quit`, `exit` or `kill` for termination commands.'
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

                os.execvp(sys_argv[0], sys_argv)
        else:
            self.errmsg('No executable file and command options recorded.')


if __name__ == '__main__':
    from trepan.processor.command import mock
    d, cp = mock.dbg_setup()
    command = RestartCommand(cp)
    command.run([])
    import sys
    if len(sys.argv) > 1:
        d.orig_sys_argv = ['python', sys.argv[0]]
        command.run([])