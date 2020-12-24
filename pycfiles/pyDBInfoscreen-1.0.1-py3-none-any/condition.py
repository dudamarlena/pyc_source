# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/condition.py
# Compiled at: 2013-03-17 12:01:36
import os
from import_relative import import_relative
Mbase_cmd = import_relative('base_cmd', top_name='pydbgr')
Mcmdfns = import_relative('cmdfns', '..', 'pydbgr')
Mfile = import_relative('file', '...lib', 'pydbgr')
Mmisc = import_relative('misc', '...', 'pydbgr')

class ConditionCommand(Mbase_cmd.DebuggerCommand):
    """**condition** *bp_number* *condition*

*bp_number* is a breakpoint number. *condition* is an expression which
must evaluate to *True* before the breakpoint is honored.  If *condition*
is absent, any existing condition is removed; i.e., the breakpoint is
made unconditional.

**Examples:**

   condition 5 x > 10  # Breakpoint 5 now has condition x > 10
   condition 5         # Remove above condition
"""
    __module__ = __name__
    aliases = ('cond', )
    category = 'breakpoints'
    min_args = 1
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Specify breakpoint number N to break only if COND is True'

    def run(self, args):
        (success, msg, bp) = self.core.bpmgr.get_breakpoint(int(args[1]))
        if not success:
            self.errmsg(msg)
            return
        if len(args) > 2:
            condition = (' ').join(args[2:])
        else:
            condition = None
            self.msg('Breakpoint %d is now unconditional.' % bp.number)
        bp.condition = condition
        return


if __name__ == '__main__':
    import sys
    Mdebugger = import_relative('debugger', '...')
    Mbreak = import_relative('break', '.')
    d = Mdebugger.Debugger()
    brkcmd = Mbreak.BreakCommand(d.core.processor)
    command = ConditionCommand(d.core.processor)
    command.proc.frame = sys._getframe()
    command.proc.setup()
    command.run(['condition', '1'])
    brkcmd.run(['break'])
    command.run(['condition', '1'])
    command.run(['condition', '1', 'x', '>', '10'])
    command.run(['condition', '1'])