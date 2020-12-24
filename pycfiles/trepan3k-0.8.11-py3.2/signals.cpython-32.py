# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/info_subcmd/signals.py
# Compiled at: 2015-05-27 09:44:41
from trepan.processor.command import base_subcmd as Mbase_subcmd
from trepan.lib import complete as Mcomplete
import columnize

class InfoSignals(Mbase_subcmd.DebuggerSubcommand):
    r"""**info signals** [*signal-name*]

**info signals** \*

Show information about how debugger treats signals to the program.
Here are the boolean actions we can take:

 * Stop: enter the debugger when the signal is sent to the debugged program

 * Print: print that the signal was received

 * Stack: show a call stack

 * Pass: pass the signal onto the program

If *signal-name* is not given, we the above show information for all
signals. If '*' is given we just give a list of signals.
 """
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