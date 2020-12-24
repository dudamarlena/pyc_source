# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/up.py
# Compiled at: 2013-03-12 21:44:02
import os
from import_relative import import_relative
Mbase_cmd = import_relative('base_cmd', '.', 'pydbgr')
Mcmdfns = import_relative('cmdfns', '..', 'pydbgr')

class UpCommand(Mbase_cmd.DebuggerCommand):
    __module__ = __name__
    category = 'stack'
    min_args = 0
    max_args = 1
    name = os.path.basename(__file__).split('.')[0]
    need_stack = True
    short_help = 'Move frame in the direction of the caller of the last-selected frame'

    def run(self, args):
        """**up** [*count*]

Move the current frame up in the stack trace (to an older frame). 0 is
the most recent frame. If no count is given, move up 1.

See also `down` and `frame`."""
        if not self.proc.stack:
            self.errmsg('Program has no stack frame set.')
            return False
        if len(args) == 1:
            count = 1
        else:
            i_stack = len(self.proc.stack)
            count_str = args[1]
            count = Mcmdfns.get_an_int(self.errmsg, count_str, ("The 'up' command argument must eval to an" + ' integer. Got: %s') % count_str, -i_stack, i_stack - 1)
            if count is None:
                return
        self.proc.adjust_frame(pos=count, absolute_pos=False)
        return False


if __name__ == '__main__':
    Mcmdproc = import_relative('cmdproc', '..')
    Mdebugger = import_relative('debugger', '...')
    d = Mdebugger.Debugger()
    cp = d.core.processor
    command = UpCommand(cp)
    command.run(['up'])

    def nest_me(cp, command, i):
        import inspect
        if i > 1:
            cp.curframe = inspect.currentframe()
            (cp.stack, cp.curindex) = Mcmdproc.get_stack(cp.curframe, None, None, cp)
            command.run(['up'])
            print '-' * 10
            command.run(['up', '-2'])
            print '-' * 10
            command.run(['up', '-3'])
            print '-' * 10
        else:
            nest_me(cp, command, i + 1)
        return


    cp.forget()
    nest_me(cp, command, 1)