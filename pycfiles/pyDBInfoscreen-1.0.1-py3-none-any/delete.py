# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/delete.py
# Compiled at: 2013-03-17 12:01:20
import os
from import_relative import import_relative
Mbase_cmd = import_relative('base_cmd', top_name='pydbgr')
Mcmdfns = import_relative('cmdfns', '..', 'pydbgr')
Mfile = import_relative('file', '...lib', 'pydbgr')
Mmisc = import_relative('misc', '...', 'pydbgr')
Mbreak = import_relative('break', '.', 'pydbgr')

class DeleteCommand(Mbase_cmd.DebuggerCommand):
    """**delete** [*bpnumber* [*bpnumber*...]]

Delete some breakpoints.

Arguments are breakpoint numbers with spaces in between.  To delete
all breakpoints, give no argument.  those breakpoints.  Without
argument, clear all breaks (but first ask confirmation).
    
See also the `clear` command which clears breakpoints by line/file
number."""
    __module__ = __name__
    category = 'breakpoints'
    min_args = 0
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Delete some breakpoints or auto-display expressions'

    def run(self, args):
        if len(args) <= 1:
            if self.confirm('Delete all breakpoints', False):
                self.core.bpmgr.delete_all_breakpoints()
            return
        for arg in args[1:]:
            i = self.proc.get_int(arg, min_value=1, default=None, cmdname='delete')
            if i is None:
                continue
            (success, msg) = self.core.bpmgr.delete_breakpoint_by_number(i)
            if not success:
                self.errmsg(msg)
            else:
                self.msg('Deleted breakpoint %d' % i)

        return


if __name__ == '__main__':
    Mdebugger = import_relative('debugger', '...')
    d = Mdebugger.Debugger()
    command = DeleteCommand(d.core.processor)