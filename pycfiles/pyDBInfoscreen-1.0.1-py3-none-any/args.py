# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/show_subcmd/args.py
# Compiled at: 2013-03-18 05:57:53
from import_relative import import_relative
Mbase_subcmd = import_relative('base_subcmd', '..', 'pydbgr')

class ShowArgs(Mbase_subcmd.DebuggerSubcommand):
    """Show argument list to give debugged program when it is started"""
    __module__ = __name__
    min_abbrev = len('arg')
    run_in_help = False

    def run(self, args):
        self.msg('Argument list to give program being debugged ' + 'when it is started is:')
        self.msg('\t%s.' % (' ').join(self.debugger.program_sys_argv[1:]))
        return False


if __name__ == '__main__':
    Mhelper = import_relative('__demo_helper__', '.', 'pydbgr')
    Mhelper.demo_run(ShowArgs)