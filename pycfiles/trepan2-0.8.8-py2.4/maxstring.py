# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/show_subcmd/maxstring.py
# Compiled at: 2015-06-06 20:11:05
from trepan.processor.command import base_subcmd as Mbase_subcmd

class ShowMaxString(Mbase_subcmd.DebuggerShowIntSubcommand):
    """**show maxstring***

Show maximum string length to use in string-oriented output

See also:
--------

`set maxstring`"""
    __module__ = __name__
    min_abbrev = len('maxs')
    short_help = 'Show max string length printed'