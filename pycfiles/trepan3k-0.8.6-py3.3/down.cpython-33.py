# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/down.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 2178 bytes
import os
from trepan.processor import frame as Mframe
from trepan.processor.command import up as Mupcmd

class DownCommand(Mupcmd.UpCommand):
    signum = 1
    name = os.path.basename(__file__).split('.')[0]
    short_help = 'Move stack frame to a more recent selected frame'

    def run(self, args):
        """**down** [*count*]

Move the current frame down in the stack trace (to a newer frame). 0
is the most recent frame. If no count is given, move down 1.

See also:
---------

`up` and `frame`."""
        Mframe.adjust_relative(self.proc, self.name, args, self.signum)
        return False


if __name__ == '__main__':
    import inspect
    from trepan.processor import cmdproc as Mcmdproc
    from trepan import debugger as Mdebugger
    d = Mdebugger.Trepan()
    cp = d.core.processor
    command = DownCommand(cp)
    command.run(['down'])

    def nest_me(cp, command, i):
        if i > 1:
            cp.curframe = inspect.currentframe()
            cp.stack, cp.curindex = Mcmdproc.get_stack(cp.curframe, None, None, cp)
            command.run(['down'])
            print('----------')
            command.run(['down', '1'])
            print('----------')
            command.run(['down', '-1'])
            print('----------')
        else:
            nest_me(cp, command, i + 1)
        return


    cp.forget()
    nest_me(cp, command, 1)