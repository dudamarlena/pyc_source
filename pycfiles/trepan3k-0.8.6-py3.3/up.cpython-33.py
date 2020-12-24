# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/up.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 2466 bytes
import os
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.processor import frame as Mframe

class UpCommand(Mbase_cmd.DebuggerCommand):
    signum = -1
    category = 'stack'
    min_args = 0
    max_args = 1
    name = os.path.basename(__file__).split('.')[0]
    need_stack = True
    short_help = 'Move frame in the direction of the caller of the last-selected frame'

    def complete(self, prefix):
        proc_obj = self.proc
        return Mframe.frame_complete(proc_obj, prefix, self.signum)

    def run(self, args):
        """**up** [*count*]

Move the current frame up in the stack trace (to an older frame). 0 is
the most recent frame. If no count is given, move up 1.

See also:
---------

`down` and `frame`."""
        Mframe.adjust_relative(self.proc, self.name, args, self.signum)
        return False


if __name__ == '__main__':
    from trepan.processor import cmdproc as Mcmdproc
    from trepan import debugger as Mdebugger
    d = Mdebugger.Trepan()
    cp = d.core.processor
    command = UpCommand(cp)
    command.run(['up'])

    def nest_me(cp, command, i):
        import inspect
        if i > 1:
            cp.curframe = inspect.currentframe()
            cp.stack, cp.curindex = Mcmdproc.get_stack(cp.curframe, None, None, cp)
            command.run(['up'])
            print('----------')
            command.run(['up', '-2'])
            print('----------')
            command.run(['up', '-3'])
            print('----------')
        else:
            nest_me(cp, command, i + 1)
        return


    cp.forget()
    nest_me(cp, command, 1)