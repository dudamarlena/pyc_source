# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/info_subcmd/globals.py
# Compiled at: 2018-03-11 10:22:50
from trepan.processor.command import base_subcmd as Mbase_subcmd
from trepan.lib import pp as Mpp

class InfoGlobals(Mbase_subcmd.DebuggerSubcommand):
    """**info globals** [*var1 ...*]

**info globals** *

With no arguments, show all of the global variables of the current stack
frame. If a list of names is provide limit display to just those
variables.

If `*` is given, just show the variable names, not the values.

See also:
---------
`info locals`, `info args`, `info frame`"""
    min_abbrev = 2
    need_stack = True
    short_help = "Show the debugged programs's global variables"

    def run(self, args):
        if not self.proc.curframe:
            self.errmsg('No frame selected.')
            return False
        names = list(self.proc.curframe.f_globals.keys())
        if len(args) > 0 and args[0] == '*':
            self.section('globals')
            self.msg(self.columnize_commands(names))
        else:
            if len(args) == 0:
                names.sort()
                for name in sorted(names):
                    val = self.proc.getval(name)
                    Mpp.pp(val, self.settings['width'], self.msg_nocr, self.msg, prefix='%s =' % name)

            else:
                for name in args:
                    if name in names:
                        val = self.proc.getval(name)
                        Mpp.pp(val, self.settings['width'], self.msg_nocr, self.msg, prefix='%s =' % name)
                        continue
                        self.errmsg('%s is not a global variable' % name)

        return False


if __name__ == '__main__':
    from trepan.processor.command import mock, info as Minfo
    d, cp = mock.dbg_setup()
    i = Minfo.InfoCommand(cp)
    sub = InfoGlobals(i)
    import inspect
    cp.curframe = inspect.currentframe()
    sub.run([])