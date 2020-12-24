# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/show_subcmd/annotate.py
# Compiled at: 2013-03-17 12:11:50
from import_relative import *
Mbase_subcmd = import_relative('base_subcmd', '..', 'pydbgr')

class ShowAnnotate(Mbase_subcmd.DebuggerShowIntSubcommand):
    """Show GNU Emacs 'annotation' level"""
    __module__ = __name__
    min_abbrev = len('an')