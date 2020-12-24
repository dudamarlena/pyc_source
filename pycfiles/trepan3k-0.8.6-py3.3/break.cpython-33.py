# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/break.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 4307 bytes
import os
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.processor import cmdbreak as Mcmdbreak
from trepan.processor import complete as Mcomplete

class BreakCommand(Mbase_cmd.DebuggerCommand):
    __doc__ = '**break** [*location*] [if *condition*]]\n\nSets a breakpoint, i.e. stopping point just before the\nexecution of the instruction specified by *location*.\n\nWithout arguments or an empty *location*, the breakpoint is set at the\ncurrent stopped location.\n\nSee `help syntax location` for detailed information on a location.\n\nIf the word `if` is given after *location*, subsequent arguments given\nWithout arguments or an empty *location*, the breakpoint is set\nthe current stopped location.\n\nNormally we only allow stopping at lines that we think are\nstoppable. If the command has a `!` suffix, force the breakpoint anyway.\n\nExamples:\n---------\n\n   break                # Break where we are current stopped at\n   break if i < j       # Break at current line if i < j\n   break 10             # Break on line 10 of the file we are\n                        # currently stopped at\n   break! 10            # Break where we are current stopped at, even if\n                        # we don\'t think line 10 is stoppable\n   break os.path.join() # Break in function os.path.join\n   break x[i].fn()      # break in function specified by x[i].fn\n   break x[i].fn() if x # break in function specified by x[i].fn\n                        # if x is set\n   break os.path:45     # Break on line 45 file holding module os.path\n   break myfile.py:2    # Break on line 2 of myfile.py\n   break myfile.py:2 if i < j # Same as above but only if i < j\n   break "foo\'s.py":1"  # One way to specify path with a quote\n   break \'c:\\foo.bat\':1      # One way to specify a Windows file name,\n   break \'/My Docs/foo.py\':1  # One way to specify path with blanks in it\n\nSee also:\n---------\n\n`tbreak`, `condition` and `help syntax location`.'
    aliases = ('b', 'break!', 'b!')
    category = 'breakpoints'
    min_args = 0
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = True
    short_help = 'Set breakpoint at specified line or function'
    complete = Mcomplete.complete_break_linenumber

    def run(self, args):
        force = True if args[0][(-1)] == '!' else False
        func, filename, lineno, condition = Mcmdbreak.parse_break_cmd(self.proc, args)
        if not (func == None and filename == None):
            Mcmdbreak.set_break(self, func, filename, lineno, condition, False, args, force=force)
        return


if __name__ == '__main__':

    def doit(cmd, a):
        cmd.current_command = ' '.join(a)
        print(Mcmdbreak.parse_break_cmd(cmd.proc, a))


    import sys
    from trepan import debugger as Mdebugger
    d = Mdebugger.Trepan()
    command = BreakCommand(d.core.processor)
    command.proc.frame = sys._getframe()
    command.proc.setup()
    doit(command, [' '])
    doit(command, ['10'])
    doit(command, [__file__ + ':10'])

    def foo():
        return 'bar'


    doit(command, ['foo'])
    doit(command, ['os.path'])
    doit(command, ['os.path', '5+1'])
    doit(command, ['os.path.join'])
    doit(command, ['if', 'True'])
    doit(command, ['foo', 'if', 'True'])
    doit(command, ['os.path:10', 'if', 'True'])
    command.run(['break'])
    command.run(['break', 'command.run'])
    command.run(['break', '10'])
    command.run(['break', __file__ + ':10'])
    command.run(['break', 'foo'])