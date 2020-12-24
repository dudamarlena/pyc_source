# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/show_subcmd/dbg_trepan.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 341 bytes
from trepan.processor.command import base_subcmd as Mbase_subcmd

class ShowDbgTrepan(Mbase_subcmd.DebuggerShowBoolSubcommand):
    __doc__ = '**show dbg_trepan**\n\nShow debugging the debugger\n\nSee also:\n---------\n\n`set dbg_trepan`'
    min_abbrev = 4
    short_help = 'Show debugging the debugger'