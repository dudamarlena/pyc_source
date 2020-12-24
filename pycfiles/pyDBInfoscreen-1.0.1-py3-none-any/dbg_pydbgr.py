# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/show_subcmd/dbg_pydbgr.py
# Compiled at: 2013-03-17 12:11:55
from import_relative import *
Mbase_subcmd = import_relative('base_subcmd', os.path.pardir)

class ShowDbgPydbgr(Mbase_subcmd.DebuggerShowBoolSubcommand):
    """Show debugging the debugger"""
    __module__ = __name__
    min_abbrev = 4