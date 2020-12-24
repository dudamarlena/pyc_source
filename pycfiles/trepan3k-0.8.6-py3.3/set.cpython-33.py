# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/set.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 1524 bytes
import os
from trepan.processor.command import base_submgr

class SetCommand(base_submgr.SubcommandMgr):
    __doc__ = '**set** *set subcommand*\n\nModifies parts of the debugger environment.\n\nYou can give unique prefix of the name of a subcommand to get\ninformation about just that subcommand.\n\nType `set` for a list of *set* subcommands and what they do.\nType `help set *` for just the list of *set* subcommands.\n'
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