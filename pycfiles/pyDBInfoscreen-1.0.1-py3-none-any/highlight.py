# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/show_subcmd/highlight.py
# Compiled at: 2013-03-17 12:26:11
from import_relative import *
Mcmdfns = import_relative('cmdfns', '...')
Mbase_subcmd = import_relative('base_subcmd', '..')

class ShowHighlight(Mbase_subcmd.DebuggerSubcommand):
    """**show highlight**

Show whether we use terminal highlighting."""
    __module__ = __name__

    def run(self, args):
        val = self.settings['highlight']
        if 'plain' == val:
            mess = 'output set to not use terminal escape sequences'
        elif 'light' == val:
            mess = 'output set for terminal with escape sequences for a light background'
        elif 'dark' == val:
            mess = 'output set for terminal with escape sequences a dark background'
        else:
            self.errmsg('Internal error: incorrect highlight setting %s' % val)
            return
        self.msg(mess)