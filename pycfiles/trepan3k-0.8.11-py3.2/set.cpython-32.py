# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/set.py
# Compiled at: 2015-04-05 10:01:28
import os
from trepan.processor.command import base_submgr

class SetCommand(base_submgr.SubcommandMgr):
    """**set** *set subcommand*

Modifies parts of the debugger environment.

You can give unique prefix of the name of a subcommand to get
information about just that subcommand.

Type `set` for a list of *set* subcommands and what they do.
Type `help set *` for just the list of *set* subcommands.
"""
    category = 'data'
    min_args = 0
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Modify parts of the debugger environment'


if __name__ == '__main__':
    from trepan.processor.command import mock
    d, cp = mock.dbg_setup()
    command = SetCommand(cp, 'set')
    command.run(['set'])