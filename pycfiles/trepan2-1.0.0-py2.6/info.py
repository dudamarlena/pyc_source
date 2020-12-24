# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/info.py
# Compiled at: 2015-02-16 15:47:50
import os
from trepan.processor.command import base_submgr as Mbase_submgr

class InfoCommand(Mbase_submgr.SubcommandMgr):
    """Generic command for showing things about the program being debugged.

You can give unique prefix of the name of a subcommand to get
information about just that subcommand.

Type `info` for a list of *info* subcommands and what they do.
Type `help info *` for just a list of *info* subcommands.
"""
    aliases = ('i', )
    category = 'status'
    min_args = 0
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Information about debugged program and its environment'


if __name__ == '__main__':
    from trepan.processor.command import mock
    (d, cp) = mock.dbg_setup()
    command = InfoCommand(cp, 'info')
    command.run(['info'])