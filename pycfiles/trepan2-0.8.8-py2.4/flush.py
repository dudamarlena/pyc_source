# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/show_subcmd/flush.py
# Compiled at: 2016-05-20 04:17:15
from trepan.processor.command import base_subcmd as Mbase_subcmd

class ShowFlush(Mbase_subcmd.DebuggerShowBoolSubcommand):
    """**show flush**

Show confirmation of potentially dangerous operations

See also:
---------

`set flush`"""
    __module__ = __name__
    min_abbrev = 3


if __name__ == '__main__':
    from trepan.processor.command.show_subcmd import __demo_helper__ as Mhelper
    Mhelper.demo_run(ShowConfirm)