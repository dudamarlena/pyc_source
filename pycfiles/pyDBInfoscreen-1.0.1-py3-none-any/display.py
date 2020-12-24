# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/info_subcmd/display.py
# Compiled at: 2013-03-24 01:16:32
from import_relative import import_relative
Mbase_subcmd = import_relative('base_subcmd', '..', 'pydbgr')
Mpp = import_relative('pp', '....lib', 'pydbgr')

class InfoDisplay(Mbase_subcmd.DebuggerSubcommand):
    """Expressions to display when program stops"""
    __module__ = __name__
    min_abbrev = 2
    need_stack = True
    short_help = 'Expressions to display when program stops'

    def run(self, args):
        lines = self.proc.display_mgr.all()
        if 0 == len(lines):
            self.errmsg('There are no auto-display expressions now.')
            return
        for line in lines:
            self.msg(line)


if __name__ == '__main__':
    mock = import_relative('mock', '..')
    Minfo = import_relative('info', '..')
    Mdebugger = import_relative('debugger', '....')
    (d, cp) = mock.dbg_setup()
    i = Minfo.InfoCommand(cp)
    sub = InfoDisplay(i)
    import inspect
    cp.curframe = inspect.currentframe()
    sub.run([])
    sub.proc.display_mgr.add(cp.curframe, '/x i')
    sub.proc.display_mgr.add(cp.curframe, 'd')
    sub.run([])