# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/show_subcmd/autolist.py
# Compiled at: 2015-06-06 18:36:26
from trepan.processor.command import base_subcmd as Mbase_subcmd

class ShowAutoList(Mbase_subcmd.DebuggerShowBoolSubcommand):
    """**show autolist**

Show debugger `list` command automatically on entry.

See also:
---------

`set autolist`"""
    min_abbrev = len('autol')
    short_help = 'Show `list` on debugger entry'


if __name__ == '__main__':
    from trepan.processor.command.show_subcmd import __demo_helper__ as Mhelper
    mgr = Mhelper.demo_run(ShowAutoList)