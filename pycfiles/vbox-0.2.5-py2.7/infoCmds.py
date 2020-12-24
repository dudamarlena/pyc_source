# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\vbox\cli\infoCmds.py
# Compiled at: 2013-03-15 12:05:06
"""Information commands."""
from . import subCmd, util

class ShowHdInfo(subCmd.PlainCall):
    changesVmState = False

    def getRcHandlers(self):
        return {1: lambda cmd, txt: None}


class ShowVmInfo(subCmd.PlainCall):
    changesVmState = False

    def getRcHandlers(self):
        return {1: lambda cmd, txt: None}

    def __call__(self, id):
        return super(ShowVmInfo, self).__call__('--details', '--machinereadable', id)