# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/kill.py
# Compiled at: 2013-03-17 22:59:28
import os
from import_relative import import_relative
Mbase_cmd = import_relative('base_cmd', top_name='pydbgr')
import signal

class KillCommand(Mbase_cmd.DebuggerCommand):
    __module__ = __name__
    category = 'running'
    min_args = 0
    max_args = 1
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Send this process a POSIX signal ("9" for "kill -9")'

    def run(self, args):
        """**kill** [**unconditionally**]

Kill execution of program being debugged.

Equivalent of `kill -KILL` *pid* where *pid* is *os.getpid()*, the current
debugged process. This is an unmaskable signal. When all else fails, e.g. in
thread code, use this.

If `unconditionally` is given, no questions are asked. Otherwise, if
we are in interactive mode, we'll prompt to make sure.
"""
        signo = signal.SIGKILL
        confirmed = False
        if len(args) <= 1:
            confirmed = self.confirm('Really do a hard kill', False)
        elif ('unconditionally').startswith(args[1]):
            confirmed = True
        else:
            try:
                signo = int(args[1])
                confirmed = True
            except ValueError:
                pass
            except TypeError:
                pass

        if confirmed:
            import os
            os.kill(os.getpid(), signo)
        return False


if __name__ == '__main__':

    def handle(*args):
        print 'signal received'


    signal.signal(28, handle)
    mock = import_relative('mock')
    (d, cp) = mock.dbg_setup()
    command = KillCommand(cp)
    command.run(['kill', 'wrong', 'number', 'of', 'args'])
    command.run(['kill', '28'])
    command.run(['kill'])