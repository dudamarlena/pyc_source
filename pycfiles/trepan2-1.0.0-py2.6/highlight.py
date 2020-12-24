# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/show_subcmd/highlight.py
# Compiled at: 2017-08-03 03:16:22
from trepan.processor.command import base_subcmd as Mbase_subcmd

class ShowHighlight(Mbase_subcmd.DebuggerSubcommand):
    """**show highlight**

Show whether we use terminal highlighting.

See also:
--------

`set highlight`"""
    short_help = 'Show if we use terminal highlight'

    def run(self, args):
        val = self.settings['highlight']
        if 'plain' == val:
            mess = 'output set to not use terminal escape sequences'
        elif 'light' == val:
            mess = 'output set for terminal with escape sequences for a light background'
        elif 'dark' == val:
            mess = 'output set for terminal with escape sequences for a dark background'
        else:
            self.errmsg('Internal error: incorrect highlight setting %s' % val)
            return
        self.msg(mess)