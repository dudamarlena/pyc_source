# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/show_subcmd/width.py
# Compiled at: 2013-01-04 05:13:40
from import_relative import *
Mbase_subcmd = import_relative('base_subcmd', '..', 'pydbgr')
Mcmdfns = import_relative('cmdfns', '...', 'pydbgr')

class ShowWidth(Mbase_subcmd.DebuggerSubcommand):
    """Show the number of characters the debugger thinks are in a line"""
    __module__ = __name__
    min_abbrev = 2

    def run(self, args):
        Mcmdfns.run_show_int(self, self.__doc__[5:].capitalize())