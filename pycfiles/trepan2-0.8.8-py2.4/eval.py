# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/eval.py
# Compiled at: 2017-08-12 23:13:24
import os
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.lib import eval as Meval

class EvalCommand(Mbase_cmd.DebuggerCommand):
    """**eval** *python-statement*

Run *python-statement* in the context of the current frame.

If no string is given, we run the string from the current source code
about to be run. If the command ends `?` (via an alias) and no string is
given, the following translations occur:

   assert = <expr>       => <expr>
   {if|elif} <expr> :    => <expr>
   while <expr> :        => <expr>
   return <expr>         => <expr>
   for <var> in <expr> : => <expr>
   <var> = <expr>        => <expr>

The above is done via regular expression matching. No fancy parsing is
done, say, to look to see if *expr* is split across a line or whether
var an assignment might have multiple variables on the left-hand side.

Examples:
---------

    eval 1+2  # 3
    eval      # Run current source-code line
    eval?     # but strips off leading 'if', 'while', ..
              # from command

See also:
---------

`deval`, `set autoeval`, `pr`, `pp` and `examine`.
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
            if self.proc.current_source_text:
                text = self.proc.current_source_text.rstrip('\n')
                if '?' == args[0][(-1)]:
                    text = Meval.extract_expression(text)
                    self.msg('eval: %s' % text)
            else:
                self.errmsg("Don't have program source text")
                return
        else:
            text = self.proc.current_command[len(self.proc.cmd_name):]
        text = text.strip()
        try:
            self.proc.exec_line(text)
        except:
            pass


if __name__ == '__main__':
    import inspect
    from trepan import debugger
    d = debugger.Debugger()
    cp = d.core.processor
    cp.curframe = inspect.currentframe()
    command = EvalCommand(cp)
    me = 10