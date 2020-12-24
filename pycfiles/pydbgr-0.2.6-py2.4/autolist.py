# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/show_subcmd/autolist.py
# Compiled at: 2013-03-18 18:59:03
from import_relative import import_relative
Mbase_subcmd = import_relative('base_subcmd', '..', 'pydbgr')

class ShowAutoList(Mbase_subcmd.DebuggerShowBoolSubcommand):
    """Show debugger *list* command automatically on entry."""
    __module__ = __name__
    min_abbrev = len('autol')


if __name__ == '__main__':
    Mhelper = import_relative('__demo_helper__', '.', 'pydbgr')
    mgr = Mhelper.demo_run(ShowAutoList)