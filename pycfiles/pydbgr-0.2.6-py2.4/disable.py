# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/disable.py
# Compiled at: 2013-03-17 12:02:00
import os
from import_relative import import_relative
Mbase_cmd = import_relative('base_cmd', top_name='pydbgr')
Mcmdfns = import_relative('cmdfns', '..', 'pydbgr')
Mfile = import_relative('file', '...lib', 'pydbgr')
Mmisc = import_relative('misc', '...', 'pydbgr')
Mbreak = import_relative('break', '.', 'pydbgr')

class DisableCommand(Mbase_cmd.DebuggerCommand):
    """**disable** *bpnumber* [*bpnumber* ...]

Disables the breakpoints given as a space separated list of breakpoint
numbers. See also `info break` to get a list.
"""
    __module__ = __name__
    category = 'breakpoints'
    min_args = 0
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Disable some breakpoints'

    def run(self, args):
        if len(args) == 1:
            self.errmsg('No breakpoint number given.')
            return
        for i in args[1:]:
            (success, msg) = self.core.bpmgr.en_disable_breakpoint_by_number(int(i), False)
            if not success:
                self.errmsg(msg)
            else:
                self.msg('Breakpoint %s disabled.' % i)


if __name__ == '__main__':
    Mdebugger = import_relative('debugger', '...')
    d = Mdebugger.Debugger()
    command = DisableCommand(d.core.processor)