# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/info_subcmd/break.py
# Compiled at: 2018-06-25 10:54:33
from trepan.processor.command import base_subcmd as Mbase_subcmd
from trepan.processor import complete as Mcomplete

class InfoBreak(Mbase_subcmd.DebuggerSubcommand):
    """**info breakpoints** [ *bp-number...* ]

Show the status of specified breakpoints (or all user-settable
breakpoints if no argument).

The **Disp* column contains one of `keep`, or `del`, to indicate the
disposition of the breakpoint after it gets hit.  `del` means that the
breakpoint will be deleted.  The **Enb** column indicates if the
breakpoint is enabled. The **Where** column indicates the file/line
number of the breakpoint.

Also shown are the number of times the breakpoint has been hit,
when that count is at least one, and any conditions the breakpoint
has.

Example:
--------

    (trepan2) info break
    Num Type          Disp Enb    Where
    1   breakpoint    del  n   at /tmp/fib.py:9
    2   breakpoint    keep y   at /tmp/fib.py:4
            breakpoint already hit 1 time
    3   breakpoint    keep y   at /tmp/fib.py:6
            stop only if x > 0

See also:
---------
`break`, `delete`, `enable`, `disable`, `condition`

    """
    min_abbrev = 1
    need_stack = False
    short_help = 'Status of user-settable breakpoints'
    complete = Mcomplete.complete_bpnumber

    def bpprint(self, bp):
        if bp.temporary:
            disp = 'del  '
        else:
            disp = 'keep '
        if bp.enabled:
            disp = disp + 'y  '
        else:
            disp = disp + 'n  '
        self.msg('%-4dbreakpoint    %s at %s:%d' % (
         bp.number, disp, self.core.filename(bp.filename), bp.line))
        if bp.condition:
            self.msg('\tstop only if %s' % bp.condition)
        if bp.ignore:
            self.msg('\tignore next %d hits' % bp.ignore)
        if bp.hits:
            if bp.hits > 1:
                ss = 's'
            else:
                ss = ''
            self.msg('\tbreakpoint already hit %d time%s' % (
             bp.hits, ss))

    def run(self, args):
        bpmgr = self.core.bpmgr
        bpnums = bpmgr.bpnumbers()
        if len(bpnums) > 0:
            if len(args) > 0:
                list_bpnums = list(set(bpnums) & set(args))
                if len(list_bpnums) == 0:
                    self.msg('No breakpoints in list given.')
                else:
                    for num_str in list_bpnums:
                        self.bpprint(bpmgr.get_breakpoint(num_str)[2])

            else:
                self.section('Num Type          Disp Enb    Where')
                for bp in bpmgr.bpbynumber:
                    if bp:
                        self.bpprint(bp)

        else:
            self.msg('No breakpoints.')


if __name__ == '__main__':
    from trepan import debugger as Mdebugger
    from trepan.processor.command import info as Minfo
    d = Mdebugger.Debugger()
    i = Minfo.InfoCommand(d.core.processor)
    sub = InfoBreak(i)
    sub.run([])