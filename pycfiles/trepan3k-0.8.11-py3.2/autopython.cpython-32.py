# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/show_subcmd/autopython.py
# Compiled at: 2015-04-06 03:51:46
from trepan.processor.command import base_subcmd as Mbase_subcmd

class ShowAutoPython(Mbase_subcmd.DebuggerShowBoolSubcommand):
    """**show autopython**

Show whether we go into a python shell when automatically when the
debugger is entered.

Change with **set autopython**
"""
    short_help = 'Show automatic Python shell entry'
    min_abbrev = len('autopy')


if __name__ == '__main__':
    from trepan.processor.command.show_subcmd import __demo_helper__ as Mhelper
    Mhelper.demo_run(ShowAutoPython)