# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/show.py
# Compiled at: 2015-04-06 05:42:01
import os
from trepan.processor.command import base_submgr as Mbase_submgr

class ShowCommand(Mbase_submgr.SubcommandMgr):
    """**show** *subcommand*

Generic command for showing things about the debugger.  You can
give unique prefix of the name of a subcommand to get information
about just that subcommand.

Type `show` for a list of *show* subcommands and what they do.
Type `help show *` for just a list of *show* subcommands.
"""
    category = 'status'
    min_args = 0
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Show parts of the debugger environment'


if __name__ == '__main__':
    from trepan.processor.command import mock
    d, cp = mock.dbg_setup()
    command = ShowCommand(cp, 'show')
    command.run(['show'])