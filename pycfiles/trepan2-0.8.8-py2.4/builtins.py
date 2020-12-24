# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/info_subcmd/builtins.py
# Compiled at: 2015-05-27 09:45:50
from trepan.processor.command import base_subcmd as Mbase_subcmd
from trepan.lib import complete as Mcomplete

class InfoBuiltins(Mbase_subcmd.DebuggerSubcommand):
    """**info builtins**

Show the builtin-functions for the current stack frame."""
    __module__ = __name__
    max_args = 1
    min_abbrev = 2
    need_stack = True
    short_help = 'Show the builtins for current stack frame'

    def complete(self, prefix):
        completions = sorted(['*'] + self.proc.curframe.f_builtins.keys())
        return Mcomplete.complete_token(completions, prefix)

    def run(self, args):
        if not self.proc.curframe:
            self.errmsg('No frame selected.')
            return False
        names = list(self.proc.curframe.f_builtins.keys())
        if len(args) > 0 and args[0] == '*':
            self.section('builtins')
            self.msg(self.columnize_commands(names))
        elif len(args) == 0:
            if len(names) > 0:
                self.section('builtins')
                self.msg(self.columnize_commands(names))
        return False


if __name__ == '__main__':
    from trepan.processor.command import mock, info as Minfo
    from trepan import debugger as Mdebugger
    d = Mdebugger.Debugger()
    (d, cp) = mock.dbg_setup(d)
    i = Minfo.InfoCommand(cp)
    sub = InfoBuiltins(i)
    import inspect
    cp.curframe = inspect.currentframe()
    sub.run([])