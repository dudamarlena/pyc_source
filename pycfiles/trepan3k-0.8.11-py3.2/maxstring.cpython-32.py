# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/set_subcmd/maxstring.py
# Compiled at: 2015-04-06 05:41:59
from trepan.processor.command import base_subcmd as Mbase_subcmd
from trepan.processor import cmdfns as Mcmdfns

class SetMaxString(Mbase_subcmd.DebuggerSubcommand):
    """**set maxstring** *number*

Set the number of characters allowed in showing string values

See also:
---------

`show maxstring`
"""
    in_list = True
    min_abbrev = len('str')
    short_help = 'Set maximum characters in showing strings'

    def run(self, args):
        Mcmdfns.run_set_int(self, ' '.join(args), "The '%s' command requires a character count" % self.name, 0, None)
        self.proc._repr.maxstring = self.settings[self.name]
        return