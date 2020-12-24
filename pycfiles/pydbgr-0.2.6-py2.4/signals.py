# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/info_subcmd/signals.py
# Compiled at: 2013-03-17 09:26:42
from import_relative import import_relative
Mbase_subcmd = import_relative('base_subcmd', '..', 'pydbgr')
Mpp = import_relative('pp', '....lib', 'pydbgr')

class InfoSignals(Mbase_subcmd.DebuggerSubcommand):
    """What debugger does when program gets various signals"""
    __module__ = __name__
    min_abbrev = 3
    need_stack = False
    short_help = 'What debugger does when program gets various signals'

    def run(self, args):
        self.debugger.sigmgr.info_signal(['signal'] + args)


if __name__ == '__main__':
    mock = import_relative('mock', '..')
    Minfo = import_relative('info', '..')
    Mdebugger = import_relative('debugger', '....')
    (d, cp) = mock.dbg_setup()
    i = Minfo.InfoCommand(cp)
    sub = InfoSignals(i)
    sub.run([])