# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/up.py
# Compiled at: 2017-10-28 10:37:24
import os
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.processor import frame as Mframe

class UpCommand(Mbase_cmd.DebuggerCommand):
    __module__ = __name__
    signum = -1
    category = 'stack'
    min_args = 0
    max_args = 1
    name = os.path.basename(__file__).split('.')[0]
    need_stack = True
    short_help = 'Move frame in the direction of the caller of the last-selected frame'

    def complete(self, prefix):
        proc_obj = self.proc
        return Mframe.frame_complete(proc_obj, prefix, self.signum)

    def run(self, args):
        """**up** [*count*]

Move the current frame up in the stack trace (to an older frame). 0 is
the most recent frame. If no count is given, move up 1.

See also:
---------

`down` and `frame`."""
        Mframe.adjust_relative(self.proc, self.name, args, self.signum)
        return False