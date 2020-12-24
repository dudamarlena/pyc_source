# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/show_subcmd/events.py
# Compiled at: 2013-03-17 12:11:58
from import_relative import *
Mbase_subcmd = import_relative('base_subcmd', os.path.pardir, 'pydbgr')
Mcmdfns = import_relative('cmdfns', '...', 'pydbgr')

class ShowEvents(Mbase_subcmd.DebuggerSubcommand):
    """Show trace events we may stop on."""
    __module__ = __name__
    min_abbrev = 2
    run_cmd = False
    run = Mcmdfns.run_show_val


if __name__ == '__main__':
    mock = import_relative('mock', '..')
    Mshow = import_relative('show', '..')
    Mdebugger = import_relative('debugger', '....')
    d = Mdebugger.Debugger()
    (d, cp) = mock.dbg_setup(d)
    i = Mshow.ShowCommand(cp)
    sub = ShowEvents(i)
    sub.run([])