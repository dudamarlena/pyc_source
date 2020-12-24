# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/show_subcmd/dbg_trepan.py
# Compiled at: 2015-06-06 20:47:39
from trepan.processor.command import base_subcmd as Mbase_subcmd

class ShowDbgTrepan(Mbase_subcmd.DebuggerShowBoolSubcommand):
    """**show dbg_trepan**

Show debugging the debugger

See also:
---------

`set dbg_trepan`"""
    __module__ = __name__
    min_abbrev = 4
    short_help = 'Show debugging the debugger'