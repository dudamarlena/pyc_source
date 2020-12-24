# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/info_subcmd/globals.py
# Compiled at: 2013-03-17 09:26:42
from import_relative import import_relative
Mbase_subcmd = import_relative('base_subcmd', '..', 'pydbgr')
Mpp = import_relative('pp', '....lib', 'pydbgr')

class InfoGlobals(Mbase_subcmd.DebuggerSubcommand):
    """Show the debugged programs's global variables"""
    __module__ = __name__
    min_abbrev = 2
    need_stack = True
    short_help = "Show the debugged programs's global variables"

    def run(self, args):
        if not self.proc.curframe:
            self.errmsg('No frame selected.')
            return False
        var_names = list(self.proc.curframe.f_globals.keys())
        var_names.sort()
        for var_name in var_names:
            val = self.proc.getval(var_name)
            Mpp.pp(val, self.settings['width'], self.msg_nocr, self.msg, prefix='%s =' % var_name)

        return False


if __name__ == '__main__':
    mock = import_relative('mock', '..')
    Minfo = import_relative('info', '..')
    Mdebugger = import_relative('debugger', '....')
    (d, cp) = mock.dbg_setup()
    i = Minfo.InfoCommand(cp)
    sub = InfoGlobals(i)
    import inspect
    cp.curframe = inspect.currentframe()
    sub.run([])