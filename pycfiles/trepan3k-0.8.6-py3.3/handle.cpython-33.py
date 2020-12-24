# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/handle.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 2763 bytes
import os
from trepan.processor.command import base_cmd as Mbase_cmd

class HandleCommand(Mbase_cmd.DebuggerCommand):
    __doc__ = '**handle** [*signal-name* [*action1* *action2* ...]]\n\nSpecify how to handle a signal *signal-name*. *signal-name* can be a\nsignal name like `SIGINT` or a signal number like 2. The absolute\nvalue is used for numbers so -9 is the same as 9 (`SIGKILL`). When\nsignal names are used, you can drop off the leading "SIG" if you want. Also\nletter case is not important either.\n\nArguments are signals and actions to apply to those signals.\nrecognized actions include `stop`, `nostop`, `print`, `noprint`,\n`pass`, `nopass`, `ignore`, or `noignore`.\n\n`stop` means reenter debugger if this signal happens (implies `print` and\n`nopass`).\n\n`Print` means print a message if this signal happens.\n\n`Pass` means let program see this signal; otherwise the program see it.\n\n`Ignore` is a synonym for `nopass`; `noignore` is a synonym for `pass`.\n\nWithout any action names the current settings are shown.\n\n**Examples:**\n\n  handle INT         # Show current settings of SIGINT\n  handle SIGINT      # same as above\n  handle int         # same as above\n  handle 2           # Probably the same as above\n  handle -2          # the same as above\n  handle INT nostop  # Don\'t stop in the debugger on SIGINT\n'
    category = 'running'
    min_args = 1
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Specify how to handle a signal'

    def run(self, args):
        if self.debugger.sigmgr.action(' '.join(args[1:])):
            if len(args) > 2:
                self.debugger.sigmgr.info_signal([args[1]])


if __name__ == '__main__':
    from trepan import debugger as Mdebugger
    d = Mdebugger.Trepan()
    command = HandleCommand(d.core.processor)
    command.run(['handle', 'USR1'])
    command.run(['handle', 'term', 'stop'])