# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/tbreak.py
# Compiled at: 2017-10-27 23:34:05
import os
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.processor import cmdbreak as Mcmdbreak
from trepan.processor import complete as Mcomplete

class TempBreakCommand(Mbase_cmd.DebuggerCommand):
    r"""**tbreak** [*location*] [**if** *condition*]

Sets a temporary breakpoint, i.e. one that is removed the after
the first time it is encountered.

See the help for location for what can be specified there.

Without arguments or an empty *location*, the temporary breakpoint is
set at the current stopped location.

If the word `if` is given after *location*, subsequent arguments given
a boolean condition which must evaluate to True before the breakpoint
is honored.

Examples:
---------

   tbreak                # Break where we are current stopped at
   tbreak if i < j       # Break at current line if i < j
   tbreak 10             # Break on line 10 of the file we are
                         # currently stopped at
   tbreak os.path.join() # Break in function os.path.join
   tbreak x[i].fn() if x # break in function specified by x[i].fn
                         # if x is set
   tbreak os.path:45     # Break on line 45 file holding module os.path
   tbreak myfile.py:45   # Break on line 45 of myfile.py
   break '''c:\foo.bat''':1"  # One way to specify a Windows file name,
   break '''/My Docs/foo.py''':1"  # One way to specify path with blanks in it

See also:
---------

`break`, `condition` and `help syntax location`.
"""
    category = 'breakpoints'
    min_args = 0
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = True
    short_help = 'Set temporary breakpoint at specified line or function'
    complete = Mcomplete.complete_break_linenumber

    def run(self, args):
        (func, filename, lineno, condition) = Mcmdbreak.parse_break_cmd(self.proc, args)
        if not (func == None and filename == None):
            Mcmdbreak.set_break(self, func, filename, lineno, condition, True, args)
        return