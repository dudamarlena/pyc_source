# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/condition.py
# Compiled at: 2015-12-01 01:33:37
import os
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.processor import complete as Mcomplete

class ConditionCommand(Mbase_cmd.DebuggerCommand):
    """**condition** *bp_number* *condition*

*bp_number* is a breakpoint number. *condition* is an expression which
must evaluate to *True* before the breakpoint is honored.  If *condition*
is absent, any existing condition is removed; i.e., the breakpoint is
made unconditional.

Examples:
---------

   condition 5 x > 10  # Breakpoint 5 now has condition x > 10
   condition 5         # Remove above condition

See also:
---------

`break`, `tbreak`."""
    aliases = ('cond', )
    category = 'breakpoints'
    min_args = 1
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Specify breakpoint number N to break only if COND is True'
    complete = Mcomplete.complete_bpnumber

    def run(self, args):
        (success, msg, bp) = self.core.bpmgr.get_breakpoint(int(args[1]))
        if not success:
            self.errmsg(msg)
            return
        else:
            if len(args) > 2:
                condition = (' ').join(args[2:])
            else:
                condition = None
                self.msg('Breakpoint %d is now unconditional.' % bp.number)
            bp.condition = condition
            return


if __name__ == '__main__':
    import sys
    from trepan import debugger as Mdebugger
    Mbreak = __import__('trepan.processor.command.break', None, None, ['*'])
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