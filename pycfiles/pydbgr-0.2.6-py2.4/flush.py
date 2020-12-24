# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/set_subcmd/flush.py
# Compiled at: 2013-03-23 10:49:58
from import_relative import import_relative
Mbase_subcmd = import_relative('base_subcmd', '..', 'pydbgr')

class SetFlush(Mbase_subcmd.DebuggerSetBoolSubcommand):
    """Set flushing output after each write"""
    __module__ = __name__
    in_list = True
    min_abbrev = len('flu')


if __name__ == '__main__':
    Mhelper = import_relative('__demo_helper__', '.', 'pydbgr')
    Mhelper.demo_run(SetFlush)