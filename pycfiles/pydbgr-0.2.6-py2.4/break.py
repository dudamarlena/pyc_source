# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/info_subcmd/break.py
# Compiled at: 2013-03-24 01:17:16
import os
from import_relative import import_relative
Mbase_subcmd = import_relative('base_subcmd', os.path.pardir)

class InfoBreak(Mbase_subcmd.DebuggerSubcommand):
    """Show breakpoints."""
    __module__ = __name__
    min_abbrev = 1
    need_stack = False
    short_help = 'Status of user-settable breakpoints'

    def bpprint(self, bp):
        if bp.temporary:
            disp = 'del  '
        else:
            disp = 'keep '
        if bp.enabled:
            disp = disp + 'y  '
        else:
            disp = disp + 'n  '
        self.msg('%-4dbreakpoint    %s at %s:%d' % (bp.number, disp, self.core.filename(bp.filename), bp.line))
        if bp.condition:
            self.msg('\tstop only if %s' % bp.condition)
        if bp.ignore:
            self.msg('\tignore next %d hits' % bp.ignore)
        if bp.hits:
            if bp.hits > 1:
                ss = 's'
            else:
                ss = ''
            self.msg('\tbreakpoint already hit %d time%s' % (bp.hits, ss))

    def run(self, args):
        bpmgr = self.core.bpmgr
        if len(bpmgr.bplist) > 0:
            self.section('Num Type          Disp Enb    Where')
            for bp in bpmgr.bpbynumber:
                if bp:
                    self.bpprint(bp)

        else:
            self.msg('No breakpoints.')


if __name__ == '__main__':
    Mdebugger = import_relative('debugger', '....', 'pydbgr')
    Minfo = import_relative('info', '..', 'pydbgr')
    d = Mdebugger.Debugger()
    i = Minfo.InfoCommand(d.core.processor)
    sub = InfoBreak(i)
    sub.run([])