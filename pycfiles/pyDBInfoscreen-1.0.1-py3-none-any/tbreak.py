# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/tbreak.py
# Compiled at: 2013-03-17 12:03:13
import os, sys
from import_relative import import_relative
Mbase_cmd = import_relative('base_cmd', top_name='pydbgr')
Mcmdfns = import_relative('cmdfns', '..', 'pydbgr')
Mfile = import_relative('file', '...lib', 'pydbgr')
Mmisc = import_relative('misc', '...', 'pydbgr')
Mcmdbreak = import_relative('cmdbreak', '..', 'pydbgr')

class TempBreakCommand(Mbase_cmd.DebuggerCommand):
    """**tbreak** [*location*] [**if** *condition*]

With a line number argument, set a break there in the current file.
With a function name, set a break at first executable line of that
function.  Without argument, set a breakpoint at current location.  If
a second argument is `if`, subequent arguments given an expression
which must evaluate to true before the breakpoint is honored.

The location line number may be prefixed with a filename or module
name and a colon. Files is searched for using *sys.path*, and the `.py`
suffix may be omitted in the file name.

**Examples:**

   tbreak     # Break where we are current stopped at
   tbreak 10  # Break on line 10 of the file we are currently stopped at
   tbreak os.path.join # Break in function os.path.join
   tbreak os.path:45   # Break on line 45 of os.path
   tbreak myfile.py:45 # Break on line 45 of myfile.py
   tbreak myfile:45    # Same as above.

See also `break`.
"""
    __module__ = __name__
    category = 'breakpoints'
    min_args = 0
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = True
    short_help = 'Set temporary breakpoint at specified line or function'

    def run(self, args):
        (func, filename, lineno, condition) = Mcmdbreak.parse_break_cmd(self, args[1:])
        Mcmdbreak.set_break(self, func, filename, lineno, condition, True, args)


if __name__ == '__main__':
    Mdebugger = import_relative('debugger', '...')
    d = Mdebugger.Debugger()
    command = TempBreakCommand(d.core.processor)
    command.proc.frame = sys._getframe()
    command.proc.setup()
    print Mcmdbreak.parse_break_cmd(command, [])
    print Mcmdbreak.parse_break_cmd(command, ['10'])
    print Mcmdbreak.parse_break_cmd(command, [__file__ + ':10'])

    def foo():
        return 'bar'


    print Mcmdbreak.parse_break_cmd(command, ['foo'])
    print Mcmdbreak.parse_break_cmd(command, ['os.path'])
    print Mcmdbreak.parse_break_cmd(command, ['os.path', '5+1'])
    print Mcmdbreak.parse_break_cmd(command, ['os.path.join'])
    print Mcmdbreak.parse_break_cmd(command, ['if', 'True'])
    print Mcmdbreak.parse_break_cmd(command, ['foo', 'if', 'True'])
    print Mcmdbreak.parse_break_cmd(command, ['os.path:10', 'if', 'True'])
    command.run(['tbreak'])
    command.run(['tbreak', 'command.run'])
    command.run(['tbreak', '10'])
    command.run(['tbreak', __file__ + ':10'])
    command.run(['tbreak', 'foo'])