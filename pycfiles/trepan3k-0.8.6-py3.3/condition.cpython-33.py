# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/condition.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 2653 bytes
import os
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.processor import complete as Mcomplete

class ConditionCommand(Mbase_cmd.DebuggerCommand):
    __doc__ = '**condition** *bp_number* *condition*\n\n*bp_number* is a breakpoint number. *condition* is an expression which\nmust evaluate to *True* before the breakpoint is honored.  If *condition*\nis absent, any existing condition is removed; i.e., the breakpoint is\nmade unconditional.\n\nExamples:\n---------\n\n   condition 5 x > 10  # Breakpoint 5 now has condition x > 10\n   condition 5         # Remove above condition\n\nSee also:\n---------\n\n`break`, `tbreak`.'
    aliases = ('cond', )
    category = 'breakpoints'
    min_args = 1
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Specify breakpoint number N to break only if COND is True'
    complete = Mcomplete.complete_bpnumber

    def run(self, args):
        success, msg, bp = self.core.bpmgr.get_breakpoint(int(args[1]))
        if not success:
            self.errmsg(msg)
            return
        else:
            if len(args) > 2:
                condition = ' '.join(args[2:])
            else:
                condition = None
                self.msg('Breakpoint %d is now unconditional.' % bp.number)
            bp.condition = condition
            return


if __name__ == '__main__':
    import sys
    from trepan import debugger as Mdebugger
    Mbreak = __import__('trepan.processor.command.break', None, None, ['*'])
    d = Mdebugger.Trepan()
    brkcmd = Mbreak.BreakCommand(d.core.processor)
    command = ConditionCommand(d.core.processor)
    command.proc.frame = sys._getframe()
    command.proc.setup()
    command.run(['condition', '1'])
    brkcmd.run(['break'])
    command.run(['condition', '1'])
    command.run(['condition', '1', 'x', '>', '10'])
    command.run(['condition', '1'])