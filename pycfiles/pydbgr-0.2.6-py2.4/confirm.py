# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/show_subcmd/confirm.py
# Compiled at: 2013-03-18 05:57:53
from import_relative import *
Mbase_subcmd = import_relative('base_subcmd', os.path.pardir)

class ShowConfirm(Mbase_subcmd.DebuggerShowBoolSubcommand):
    """Show confirmation of potentially dangerous operations"""
    __module__ = __name__
    min_abbrev = 3


if __name__ == '__main__':
    Mhelper = import_relative('__demo_helper__', '.', 'pydbgr')
    Mhelper.demo_run(ShowConfirm)