# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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