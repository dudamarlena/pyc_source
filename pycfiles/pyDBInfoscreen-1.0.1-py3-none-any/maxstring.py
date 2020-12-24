# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/show_subcmd/maxstring.py
# Compiled at: 2013-01-04 05:13:40
from import_relative import *
Mbase_subcmd = import_relative('base_subcmd', '..', 'pydbgr')

class ShowMaxString(Mbase_subcmd.DebuggerShowIntSubcommand):
    """Show maximum string length to use in string-oriented output"""
    __module__ = __name__
    min_abbrev = 2