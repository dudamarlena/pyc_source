# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/enable.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 2283 bytes
import os
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.processor import complete as Mcomplete

class EnableCommand(Mbase_cmd.DebuggerCommand):
    __doc__ = '**enable** *bpnumber* [*bpnumber* ...]\n\nEnables the breakpoints given as a space separated list of breakpoint\nnumbers. To enable all breakpoints, give no argument. See also `info break` to get a list.\n\nSee also:\n---------\n`disable`\n'
    aliases = ('en', )
    category = 'breakpoints'
    min_args = 0
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Enable some breakpoints'
    complete = Mcomplete.complete_bpnumber

    def run(self, args):
        if len(args) == 1:
            self.msg(self.core.bpmgr.en_disable_all_breakpoints(do_enable=True))
            return
        for i in args[1:]:
            success, msg = self.core.bpmgr.en_disable_breakpoint_by_number(i, do_enable=True)
            if not success:
                self.errmsg(msg)
            else:
                self.msg('Breakpoint %s enabled.' % i)


if __name__ == '__main__':
    from trepan import debugger as Mdebugger
    d = Mdebugger.Trepan()
    command = EnableCommand(d.core.processor)