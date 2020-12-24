# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/show_subcmd/autoeval.py
# Compiled at: 2015-06-06 20:55:59
from trepan.processor.command import base_subcmd as Mbase_subcmd

class ShowAutoEval(Mbase_subcmd.DebuggerShowBoolSubcommand):
    """**show autoeval**

Show Python evaluation of unrecognized debugger commands.

See also:
---------

`set autoeval`
"""
    min_abbrev = len('autoe')


if __name__ == '__main__':
    from trepan.processor.command.show_subcmd import __demo_helper__ as Mhelper
    Mhelper.demo_run(ShowAutoEval)