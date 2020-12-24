# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/handle.py
# Compiled at: 2015-02-16 15:47:50
import os
from trepan.processor.command import base_cmd as Mbase_cmd

class HandleCommand(Mbase_cmd.DebuggerCommand):
    """**handle** [*signal-name* [*action1* *action2* ...]]

Specify how to handle a signal *signal-name*. *signal-name* can be a
signal name like `SIGINT` or a signal number like 2. The absolute
value is used for numbers so -9 is the same as 9 (`SIGKILL`). When
signal names are used, you can drop off the leading "SIG" if you want. Also
letter case is not important either.

Arguments are signals and actions to apply to those signals.
recognized actions include `stop`, `nostop`, `print`, `noprint`,
`pass`, `nopass`, `ignore`, or `noignore`.

`stop` means reenter debugger if this signal happens (implies `print` and
`nopass`).

`Print` means print a message if this signal happens.

`Pass` means let program see this signal; otherwise the program see it.

`Ignore` is a synonym for `nopass`; `noignore` is a synonym for `pass`.

Without any action names the current settings are shown.

**Examples:**

  handle INT         # Show current settings of SIGINT
  handle SIGINT      # same as above
  handle int         # same as above
  handle 2           # Probably the same as above
  handle -2          # the same as above
  handle INT nostop  # Don't stop in the debugger on SIGINT
"""
    __module__ = __name__
    category = 'running'
    min_args = 1
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Specify how to handle a signal'

    def run(self, args):
        if self.debugger.sigmgr.action((' ').join(args[1:])) and len(args) > 2:
            self.debugger.sigmgr.info_signal([args[1]])


if __name__ == '__main__':
    from trepan import debugger as Mdebugger
    d = Mdebugger.Debugger()
    command = HandleCommand(d.core.processor)
    command.run(['handle', 'USR1'])
    command.run(['handle', 'term', 'stop'])