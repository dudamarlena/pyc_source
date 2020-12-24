# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/eval.py
# Compiled at: 2013-01-12 03:14:27
import os
from import_relative import import_relative
Mbase_cmd = import_relative('base_cmd', top_name='pydbgr')
Mprint = import_relative('print', '...lib', 'pydbgr')
Meval = import_relative('eval', '...lib', 'pydbgr')

class EvalCommand(Mbase_cmd.DebuggerCommand):
    """**eval** *python-statement*

Run *python-statement* in the context of the current frame.

If no string is given, we run the string from the current source code
about to be run. If the command ends `?` (via an alias) and no string is
given, the following translations occur:

   {if|elif} <expr> :  => <expr>
   while <expr> :      => <expr>
   return <expr>       => <expr>
   <var> = <expr>      => <expr>

The above is done via regular expression matching. No fancy parsing is
done, say, to look to see if *expr* is split across a line or whether
var an assignment might have multiple variables on the left-hand side.

**Examples:**

    eval 1+2  # 3
    eval      # Run current source-code line
    eval?     # but strips off leading 'if', 'while', ..
              # from command

See also `set autoeval`, `pr`, `pp` and `examine`.
"""
    __module__ = __name__
    aliases = ('eval?', '?')
    category = 'data'
    min_args = 0
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = True
    short_help = 'Print value of expression EXP'

    def run(self, args):
        if 1 == len(args):
            text = self.proc.current_source_text.rstrip('\n')
            if '?' == args[0][(-1)]:
                text = Meval.extract_expression(text)
                self.msg('eval: %s' % text)
        else:
            text = self.proc.current_command[len(self.proc.cmd_name):]
        text = text.strip()
        try:
            self.proc.exec_line(text)
        except:
            pass


if __name__ == '__main__':
    import inspect
    cmdproc = import_relative('cmdproc', '..')
    debugger = import_relative('debugger', '...')
    d = debugger.Debugger()
    cp = d.core.processor
    cp.curframe = inspect.currentframe()
    command = EvalCommand(cp)
    me = 10