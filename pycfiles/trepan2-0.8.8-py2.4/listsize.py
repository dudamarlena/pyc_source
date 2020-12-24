# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/show_subcmd/listsize.py
# Compiled at: 2015-06-06 20:12:07
from trepan.processor.command import base_subcmd as Mbase_subcmd

class ShowListSize(Mbase_subcmd.DebuggerShowIntSubcommand):
    """**show maxstring***

Show the number lines printed in a 'list' command by default

See also:
--------

`set listsize`"""
    __module__ = __name__
    min_abbrev = len('lis')
    short_help = 'Show number of lines in `list`'