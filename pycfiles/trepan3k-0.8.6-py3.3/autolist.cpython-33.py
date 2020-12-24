# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/show_subcmd/autolist.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 1230 bytes
from trepan.processor.command import base_subcmd as Mbase_subcmd

class ShowAutoList(Mbase_subcmd.DebuggerShowBoolSubcommand):
    __doc__ = '**show autolist**\n\nShow debugger `list` command automatically on entry.\n\nSee also:\n---------\n\n`set autolist`'
    min_abbrev = len('autol')
    short_help = 'Show `list` on debugger entry'


if __name__ == '__main__':
    from trepan.processor.command.show_subcmd import __demo_helper__ as Mhelper
    Mhelper.demo_run(ShowAutoList)