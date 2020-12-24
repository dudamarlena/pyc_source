# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/pr.py
# Compiled at: 2013-03-22 02:52:57
import os
from import_relative import import_relative
Mbase_cmd = import_relative('base_cmd', top_name='pydbgr')
Mprint = import_relative('print', '...lib', 'pydbgr')

class PrCommand(Mbase_cmd.DebuggerCommand):
    """**pr** *expression*

Print the value of the expression. Variables accessible are those of the
environment of the selected stack frame, plus globals. 

The expression may be preceded with */fmt* where *fmt* is one of the
format letters 'c', 'x', 'o', 'f', or 's' for chr, hex, oct, 
float or str respectively.

If the length output string large, the first part of the value is
shown and `...` indicates it has been truncated

See also `pp` and `examine` for commands which do more in the way of
formatting.
"""
    __module__ = __name__
    category = 'data'
    min_args = 1
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = True
    short_help = 'Print value of expression EXP'

    def run(self, args):
        if len(args) > 2 and '/' == args[1][0]:
            fmt = args[1]
            del args[1]
        else:
            fmt = None
        arg = (' ').join(args[1:])
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
    mock = import_relative('mock')
    (d, cp) = mock.dbg_setup()
    cp.curframe = inspect.currentframe()
    command = PrCommand(cp)
    me = 10
    command.run([command.name, 'me'])
    command.run([command.name, '/x', 'me'])
    command.run([command.name, '/o', 'me'])