# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/pp.py
# Compiled at: 2013-03-22 02:54:08
import os
from import_relative import import_relative
Mbase_cmd = import_relative('base_cmd', '.', 'pydbgr')
Mdebugger = import_relative('debugger', '...', 'pydbgr')
Mpp = import_relative('pp', '...lib', 'pydbgr')

class PrettyPrintCommand(Mbase_cmd.DebuggerCommand):
    """**pp** *expression*

Pretty-print the value of the expression.

Simple arrays are shown columnized horizontally. Other values are printed
via *pprint.pformat()*.

See also `pr` and `examine` for commands which do more in the way of
formatting.
"""
    __module__ = __name__
    category = 'data'
    min_args = 1
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Pretty print value of expression EXP'

    def run(self, args):
        arg = (' ').join(args[1:])
        val = self.proc.eval(arg)
        Mpp.pp(val, self.settings['width'], self.msg_nocr, self.msg)
        return False


if __name__ == '__main__':
    import inspect
    mock = import_relative('mock')
    (d, cp) = mock.dbg_setup()
    cp.curframe = inspect.currentframe()
    command = PrettyPrintCommand(cp)
    me = list(range(10))
    command.run(['pp', 'me'])
    me = list(range(100))
    command.run(['pp', 'me'])
    import sys
    command.run(['pp', 'sys.modules.keys()'])
    me = 'fooled you'
    command.run(['pp', 'locals()'])