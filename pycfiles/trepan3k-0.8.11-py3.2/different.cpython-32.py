# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/set_subcmd/different.py
# Compiled at: 2016-06-21 23:49:58
from trepan.processor.command import base_subcmd as Mbase_subcmd

class SetDifferent(Mbase_subcmd.DebuggerSetBoolSubcommand):
    """**set different** [ **on** | **off** ]

Set different line location between consecutive debugger stops.

By default, the debugger traces all events possible including line,
exceptions, call and return events. Just this alone may mean that for
any given source line several consecutive stops at a given line may
occur. Independent of this, Python allows one to put several commands
in a single source line of code. When a programmer does this, it might
be because the programmer thinks of the line as one unit.

One of the challenges of debugging is getting the granualarity of
stepping comfortable. Because of the above, stepping all events can
often be too fine-grained and annoying. By setting different on you
can set a more coarse-level of stepping which often still is small
enough that you won't miss anything important.
Note that the `step` and `next` debugger commands have `+` and `-`
suffixes if you wan to override this setting on a per-command basis.

See also:
---------
`set trace` to change what events you want to filter.
`show trace`
"""
    in_list = True
    min_abbrev = len('dif')


if __name__ == '__main__':
    from trepan.processor.command.set_subcmd import __demo_helper__ as Mhelper
    Mhelper.demo_run(SetDifferent)