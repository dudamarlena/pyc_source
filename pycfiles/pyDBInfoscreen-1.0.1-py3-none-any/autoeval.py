# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/show_subcmd/autoeval.py
# Compiled at: 2013-03-18 05:57:53
from import_relative import *
Mbase_subcmd = import_relative('base_subcmd', '..')

class ShowAutoEval(Mbase_subcmd.DebuggerShowBoolSubcommand):
    """Show Python evaluation of unrecognized debugger commands"""
    __module__ = __name__
    min_abbrev = len('autoe')


if __name__ == '__main__':
    Mhelper = import_relative('__demo_helper__', '.', 'pydbgr')
    Mhelper.demo_run(ShowAutoEval)