# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/show.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 1566 bytes
import os
from trepan.processor.command import base_submgr as Mbase_submgr

class ShowCommand(Mbase_submgr.SubcommandMgr):
    __doc__ = '**show** *subcommand*\n\nGeneric command for showing things about the debugger.  You can\ngive unique prefix of the name of a subcommand to get information\nabout just that subcommand.\n\nType `show` for a list of *show* subcommands and what they do.\nType `help show *` for just a list of *show* subcommands.\n'
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