# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/eval.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 3084 bytes
import os
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.lib import eval as Meval

class EvalCommand(Mbase_cmd.DebuggerCommand):
    __doc__ = "**eval** *python-statement*\n\nRun *python-statement* in the context of the current frame.\n\nIf no string is given, we run the string from the current source code\nabout to be run. If the command ends `?` (via an alias) and no string is\ngiven, the following translations occur:\n\n   assert = <expr>       => <expr>\n   {if|elif} <expr> :    => <expr>\n   while <expr> :        => <expr>\n   return <expr>         => <expr>\n   for <var> in <expr> : => <expr>\n   <var> = <expr>        => <expr>\n\nThe above is done via regular expression matching. No fancy parsing is\ndone, say, to look to see if *expr* is split across a line or whether\nvar an assignment might have multiple variables on the left-hand side.\n\nExamples:\n---------\n\n    eval 1+2  # 3\n    eval      # Run current source-code line\n    eval?     # but strips off leading 'if', 'while', ..\n              # from command\n\nSee also:\n---------\n\n`deval`, `set autoeval`, `pr`, `pp` and `examine`.\n"
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
    d = debugger.Trepan()
    cp = d.core.processor
    cp.curframe = inspect.currentframe()
    command = EvalCommand(cp)
    me = 10