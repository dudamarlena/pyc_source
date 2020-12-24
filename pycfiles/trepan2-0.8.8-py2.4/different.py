# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/show_subcmd/different.py
# Compiled at: 2015-06-06 20:13:52
from trepan.processor.command import base_subcmd as Mbase_subcmd

class ShowDifferent(Mbase_subcmd.DebuggerShowBoolSubcommand):
    """**show different**

Show whether stop on different file/line positions

See also:
--------

`set different`"""
    __module__ = __name__
    min_abbrev = 3