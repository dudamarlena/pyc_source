# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/p.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 2558 bytes
import os
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.lib import printing as Mprint
from trepan.processor import complete as Mcomplete

class PCommand(Mbase_cmd.DebuggerCommand):
    __doc__ = "**print** *expression*\n\nPrint the value of the expression. Variables accessible are those of the\nenvironment of the selected stack frame, plus globals.\n\nThe expression may be preceded with */fmt* where *fmt* is one of the\nformat letters 'c', 'x', 'o', 'f', or 's' for chr, hex, oct,\nfloat or str respectively.\n\nIf the length output string large, the first part of the value is\nshown and `...` indicates it has been truncated.\n\nSee also:\n---------\n\n `pp` and `examine` for commands which do more in the way of formatting.\n"
    aliases = ('print', 'pr')
    category = 'data'
    min_args = 1
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = True
    short_help = 'Print value of expression EXP'
    complete = Mcomplete.complete_identifier

    def run(self, args):
        if len(args) > 2 and '/' == args[1][0]:
            fmt = args[1]
            del args[1]
        else:
            fmt = None
        arg = ' '.join(args[1:])
        try:
            val = self.proc.eval(arg)
            if fmt:
                val = Mprint.printf(val, fmt)
            self.msg(self.proc._saferepr(val))
        except:
            pass

        return


if __name__ == '__main__':
    import inspect
    from trepan.processor.command import mock
    d, cp = mock.dbg_setup()
    cp.curframe = inspect.currentframe()
    command = PCommand(cp)
    me = 10
    command.run([command.name, 'me'])
    command.run([command.name, '/x', 'me'])
    command.run([command.name, '/o', 'me'])