# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/examine.py
# Compiled at: 2015-06-03 13:30:16
import os
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.lib import printing as Mprint

class ExamineCommand(Mbase_cmd.DebuggerCommand):
    """**examine** *expr1* [*expr2* ...]

Examine value, type and object attributes of an expression.

In contrast to normal Python expressions, expressions should not have
blanks which would cause shlex to see them as different tokens.

Examples:
---------

    examine x+1   # ok
    examine x + 1 # not ok

See also:
---------

`pr`, `pp`, and `whatis`.
"""
    aliases = ('x', )
    category = 'data'
    min_args = 1
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = True
    short_help = 'Examine value, type, and object attributes of an expression'

    def run(self, args):
        for arg in args[1:]:
            s = Mprint.print_obj(arg, self.proc.curframe)
            self.msg(s)


if __name__ == '__main__':
    import inspect
    from trepan import debugger
    d = debugger.Trepan()
    cp = d.core.processor
    cp.curframe = inspect.currentframe()
    command = ExamineCommand(cp)
    command.run(['examine', '10'])
    me = []
    print('=' * 30)
    command.run(['examine', 'me'])
    print('=' * 30)
    command.run(['examine', 'Mbase_cmd.DebuggerCommand'])