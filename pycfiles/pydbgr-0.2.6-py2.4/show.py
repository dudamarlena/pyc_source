# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/show.py
# Compiled at: 2013-03-16 20:36:17
import os
from import_relative import import_relative
Mbase_submgr = import_relative('base_submgr')

class ShowCommand(Mbase_submgr.SubcommandMgr):
    """Generic command for showing things about the debugger.  You can
give unique prefix of the name of a subcommand to get information
about just that subcommand.

Type `show` for a list of *show* subcommands and what they do.
Type `help show *` for just a list of *show* subcommands.
"""
    __module__ = __name__
    category = 'status'
    min_args = 0
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Show parts of the debugger environment'

    def summary_help(self, subcmd_name, subcmd):
        self.msg_nocr('%-13s(%d): ' % (subcmd_name, subcmd.min_abbrev))
        if subcmd.run_in_help and subcmd.run_cmd:
            return subcmd.run([])
        else:
            self.rst_msg('%s.' % subcmd.short_help)


if __name__ == '__main__':
    mock = import_relative('mock')
    (d, cp) = mock.dbg_setup()
    command = ShowCommand(cp, 'show')
    command.run(['show'])