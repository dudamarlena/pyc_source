# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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