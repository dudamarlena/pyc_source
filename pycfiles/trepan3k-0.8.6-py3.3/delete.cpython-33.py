# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/delete.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 2444 bytes
import os
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.processor import complete as Mcomplete

class DeleteCommand(Mbase_cmd.DebuggerCommand):
    __doc__ = '**delete** [*bpnumber* [*bpnumber*...]]\n\nDelete some breakpoints.\n\nArguments are breakpoint numbers with spaces in between.  To delete\nall breakpoints, give no argument.  Without\narguments, clear all breaks (but first ask for confirmation).\n\nSee also:\n---------\n`clear`\n'
    category = 'breakpoints'
    aliases = ('delete!', )
    min_args = 0
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Delete some breakpoints or auto-display expressions'
    complete = Mcomplete.complete_bpnumber

    def run(self, args):
        if len(args) <= 1:
            if '!' != args[0][(-1)]:
                confirmed = self.confirm('Delete all breakpoints', False)
            else:
                confirmed = True
            if confirmed:
                self.msg(self.core.bpmgr.delete_all_breakpoints())
            return
        else:
            for arg in args[1:]:
                i = self.proc.get_int(arg, min_value=1, default=None, cmdname='delete')
                if i is None:
                    continue
                success, msg = self.core.bpmgr.delete_breakpoint_by_number(i)
                if not success:
                    self.errmsg(msg)
                else:
                    self.msg('Deleted breakpoint %d' % i)

            return


if __name__ == '__main__':
    from trepan import debugger as Mdebugger
    d = Mdebugger.Trepan()
    command = DeleteCommand(d.core.processor)