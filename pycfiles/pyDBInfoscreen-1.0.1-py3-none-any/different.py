# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/show_subcmd/different.py
# Compiled at: 2013-01-04 05:13:40
from import_relative import import_relative
Mbase_subcmd = import_relative('base_subcmd', '..', 'pydbgr')

class ShowDifferent(Mbase_subcmd.DebuggerShowBoolSubcommand):
    """Show consecutive stops on different file/line positions"""
    __module__ = __name__
    min_abbrev = 3