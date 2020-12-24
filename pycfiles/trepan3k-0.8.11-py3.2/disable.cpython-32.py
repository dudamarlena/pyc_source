# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/disable.py
# Compiled at: 2017-09-07 04:14:06
import os
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.processor import complete as Mcomplete

class DisableCommand(Mbase_cmd.DebuggerCommand):
    """**disable** *bpnumber* [*bpnumber* ...]

Disables the breakpoints given as a space separated list of breakpoint
numbers. To disable all breakpoints, give no argument. See also `info break` to get a list.

See also:
---------
`enable`
"""
    category = 'breakpoints'
    min_args = 0
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Disable some breakpoints'
    complete = Mcomplete.complete_bpnumber

    def run(self, args):
        if len(args) == 1:
            self.msg(self.core.bpmgr.en_disable_all_breakpoints(do_enable=False))
            return
        for i in args[1:]:
            success, msg = self.core.bpmgr.en_disable_breakpoint_by_number(int(i), False)
            if not success:
                self.errmsg(msg)
            else:
                self.msg('Breakpoint %s disabled.' % i)


if __name__ == '__main__':
    from trepan import debugger as Mdebugger
    d = Mdebugger.Trepan()
    command = DisableCommand(d.core.processor)