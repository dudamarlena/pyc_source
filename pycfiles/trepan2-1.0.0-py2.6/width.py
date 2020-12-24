# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/show_subcmd/width.py
# Compiled at: 2015-02-17 12:15:19
from trepan.processor.command import base_subcmd as Mbase_subcmd
from trepan.processor import cmdfns as Mcmdfns

class ShowWidth(Mbase_subcmd.DebuggerSubcommand):
    """Show the number of characters the debugger thinks are in a line"""
    min_abbrev = len('wi')
    short_help = 'Show terminal width'

    def run(self, args):
        Mcmdfns.run_show_int(self, self.__doc__[5:].capitalize())