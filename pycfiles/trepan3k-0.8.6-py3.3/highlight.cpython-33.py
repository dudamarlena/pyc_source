# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/show_subcmd/highlight.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 1721 bytes
from trepan.processor.command import base_subcmd as Mbase_subcmd

class ShowHighlight(Mbase_subcmd.DebuggerSubcommand):
    __doc__ = '**show highlight**\n\nShow whether we use terminal highlighting.\n\nSee also:\n--------\n\n`set highlight`'
    short_help = 'Show if we use terminal highlight'

    def run(self, args):
        val = self.settings['highlight']
        if 'plain' == val:
            mess = 'output set to not use terminal escape sequences'
        else:
            if 'light' == val:
                mess = 'output set for terminal with escape sequences for a light background'
            else:
                if 'dark' == val:
                    mess = 'output set for terminal with escape sequences for a dark background'
                else:
                    self.errmsg('Internal error: incorrect highlight setting %s' % val)
                    return
        self.msg(mess)