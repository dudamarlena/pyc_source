# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/info_subcmd/locals.py
# Compiled at: 2018-06-25 10:54:26
import re
from trepan.processor.command import base_subcmd as Mbase_subcmd
from trepan.lib import pp as Mpp
from trepan.lib import complete as Mcomplete
_with_local_varname = re.compile('_\\[[0-9+]\\]')

class InfoLocals(Mbase_subcmd.DebuggerSubcommand):
    """**info locals** [*var1 ...*]

**info locals** *

With no arguments, show all of the local variables of the current stack
frame. If a list of names is provide limit display to just those
variables.

If `*` is given, just show the variable names, not the values.

See also:
---------
`info globals`, `info args`, `info frame`
"""
    min_abbrev = 2
    need_stack = True
    short_help = 'Show the local variables of current stack frame'

    def complete(self, prefix):
        completions = sorted(['*'] + self.proc.curframe.f_locals.keys())
        return Mcomplete.complete_token(completions, prefix)

    def run(self, args):
        if not self.proc.curframe:
            self.errmsg('No frame selected')
            return False
        names = list(self.proc.curframe.f_locals.keys())
        if len(args) > 0 and args[0] == '*':
            self.section('locals')
            self.msg(self.columnize_commands(names))
        elif len(args) == 0:
            for name in sorted(names):
                if _with_local_varname.match(name):
                    val = self.proc.curframe.f_locals[name]
                else:
                    val = self.proc.getval(name)
                Mpp.pp(val, self.settings['width'], self.msg_nocr, self.msg, prefix='%s =' % name)

        for name in args:
            if name in names:
                if _with_local_varname.match(name):
                    val = self.proc.curframe.f_locals[name]
                else:
                    val = self.proc.getval(name)
                Mpp.pp(val, self.settings['width'], self.msg_nocr, self.msg, prefix='%s =' % name)
            else:
                self.errmsg('%s is not a local variable' % name)

        return False


if __name__ == '__main__':
    from trepan.processor.command import mock, info as Minfo
    from trepan import debugger as Mdebugger
    d = Mdebugger.Debugger()
    (d, cp) = mock.dbg_setup(d)
    i = Minfo.InfoCommand(cp)
    sub = InfoLocals(i)
    l = list(range(30))
    import inspect
    cp.curframe = inspect.currentframe()
    sub.run([])
    sub.run(['*'])
    sub.run(['Minfo'])