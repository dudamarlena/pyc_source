# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/show_subcmd/dbg_pydbgr.py
# Compiled at: 2013-03-17 12:11:55
from import_relative import *
Mbase_subcmd = import_relative('base_subcmd', os.path.pardir)

class ShowDbgPydbgr(Mbase_subcmd.DebuggerShowBoolSubcommand):
    """Show debugging the debugger"""
    __module__ = __name__
    min_abbrev = 4