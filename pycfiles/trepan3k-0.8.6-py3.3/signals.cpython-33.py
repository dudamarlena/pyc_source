# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/info_subcmd/signals.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 2200 bytes
from trepan.processor.command import base_subcmd as Mbase_subcmd
from trepan.lib import complete as Mcomplete
import columnize

class InfoSignals(Mbase_subcmd.DebuggerSubcommand):
    __doc__ = "**info signals** [*signal-name*]\n\n**info signals** \\*\n\nShow information about how debugger treats signals to the program.\nHere are the boolean actions we can take:\n\n * Stop: enter the debugger when the signal is sent to the debugged program\n\n * Print: print that the signal was received\n\n * Stack: show a call stack\n\n * Pass: pass the signal onto the program\n\nIf *signal-name* is not given, we the above show information for all\nsignals. If '*' is given we just give a list of signals.\n "
    min_abbrev = 3
    need_stack = False
    short_help = 'What debugger does when program gets various signals'

    def complete(self, prefix):
        completions = sorted(['*'] + self.debugger.sigmgr.siglist)
        return Mcomplete.complete_token(completions, prefix)

    def run(self, args):
        if len(args) > 0 and args[0] == '*':
            self.msg(self.columnize_commands(self.debugger.sigmgr.siglist))
        else:
            self.debugger.sigmgr.info_signal(['signal'] + args)


if __name__ == '__main__':
    from trepan.processor.command import mock, info as Minfo
    d, cp = mock.dbg_setup()
    i = Minfo.InfoCommand(cp)
    sub = InfoSignals(i)