# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/set_subcmd/cmdtrace.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 1315 bytes
from trepan.processor.command import base_subcmd as Mbase_subcmd
from trepan.processor import cmdfns as Mcmdfns

class SetCmdtrace(Mbase_subcmd.DebuggerSetBoolSubcommand):
    __doc__ = 'Set echoing lines read from debugger command files'
    in_list = True
    min_abbrev = len('cmdt')

    def run(self, args):
        Mcmdfns.run_set_bool(self, args)
        dbg = self.debugger
        if hasattr(dbg.intf[(-1)], 'verbose'):
            dbg.intf[(-1)].verbose = dbg.settings[self.name]