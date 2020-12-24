# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/set_subcmd/different.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 2178 bytes
from trepan.processor.command import base_subcmd as Mbase_subcmd

class SetDifferent(Mbase_subcmd.DebuggerSetBoolSubcommand):
    __doc__ = "**set different** [ **on** | **off** ]\n\nSet different line location between consecutive debugger stops.\n\nBy default, the debugger traces all events possible including line,\nexceptions, call and return events. Just this alone may mean that for\nany given source line several consecutive stops at a given line may\noccur. Independent of this, Python allows one to put several commands\nin a single source line of code. When a programmer does this, it might\nbe because the programmer thinks of the line as one unit.\n\nOne of the challenges of debugging is getting the granualarity of\nstepping comfortable. Because of the above, stepping all events can\noften be too fine-grained and annoying. By setting different on you\ncan set a more coarse-level of stepping which often still is small\nenough that you won't miss anything important.\nNote that the `step` and `next` debugger commands have `+` and `-`\nsuffixes if you wan to override this setting on a per-command basis.\n\nSee also:\n---------\n`set trace` to change what events you want to filter.\n`show trace`\n"
    in_list = True
    min_abbrev = len('dif')


if __name__ == '__main__':
    from trepan.processor.command.set_subcmd import __demo_helper__ as Mhelper
    Mhelper.demo_run(SetDifferent)