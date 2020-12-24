# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/show_subcmd/cmdtrace.py
# Compiled at: 2015-06-06 20:46:59
from trepan.processor.command import base_subcmd as Mbase_subcmd

class ShowCmdtrace(Mbase_subcmd.DebuggerShowBoolSubcommand):
    """*show cmdtrace**

Show debugger commands before running them
See also:
---------

`set cmdtrace`"""
    min_abbrev = 4
    short_help = 'Show debugger commands before running them'