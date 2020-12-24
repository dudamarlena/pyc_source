# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/set.py
# Compiled at: 2013-01-07 06:17:14
import os
from import_relative import import_relative
base_submgr = import_relative('base_submgr', top_name='pydbgr')

class SetCommand(base_submgr.SubcommandMgr):
    """Modifies parts of the debugger environment.

You can give unique prefix of the name of a subcommand to get
information about just that subcommand.

Type `set` for a list of *set* subcommands and what they do.
Type `help set *` for just the list of *set* subcommands.
"""
    __module__ = __name__
    category = 'data'
    min_args = 0
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Modify parts of the debugger environment'


if __name__ == '__main__':
    mock = import_relative('mock')
    (d, cp) = mock.dbg_setup()
    command = SetCommand(cp, 'set')
    command.run(['set'])