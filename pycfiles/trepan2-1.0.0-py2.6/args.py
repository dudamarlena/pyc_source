# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/show_subcmd/args.py
# Compiled at: 2015-02-17 12:15:19
from trepan.processor.command import base_subcmd as Mbase_subcmd

class ShowArgs(Mbase_subcmd.DebuggerSubcommand):
    """Show argument list to give debugged program when it is started"""
    min_abbrev = len('arg')
    run_in_help = False
    short_help = 'Show arguments when program is started'

    def run(self, args):
        self.msg('Argument list to give program being debugged ' + 'when it is started is:')
        self.msg('\t%s.' % (' ').join(self.debugger.program_sys_argv[1:]))
        return False


if __name__ == '__main__':
    from trepan.processor.command.show_subcmd import __demo_helper__ as Mhelper
    Mhelper.demo_run(ShowArgs)