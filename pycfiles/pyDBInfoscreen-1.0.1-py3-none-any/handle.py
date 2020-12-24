# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/handle.py
# Compiled at: 2013-01-11 18:05:09
import os
from import_relative import import_relative
Mbase_cmd = import_relative('base_cmd')
Msig = import_relative('sighandler', '...lib', 'pydbgr')

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
    Mdebugger = import_relative('debugger', '...')
    d = Mdebugger.Debugger()
    command = HandleCommand(d.core.processor)
    command.run(['handle', 'USR1'])
    command.run(['handle', 'term', 'stop'])