# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\vbox\cli\cliInterface.py
# Compiled at: 2013-03-20 09:41:35
import threading
from ..pyVb import base
from .vboxManage import VBoxManage
from . import util

class CommandLineInterface(base.VirtualBoxElement):

    def __init__(self, *args, **kwargs):
        super(CommandLineInterface, self).__init__(*args, **kwargs)
        self.cliAccessLock = threading.RLock()
        self.manage = VBoxManage(self)
        self.util = util
        self.programs = (
         self.manage,)

    def addPreCmdExecListener(self, cb):
        _cancellers = [ exc.addPreCmdExecListener(cb) for exc in self.programs
                      ]
        return lambda : [ fn() for fn in _cancellers ]

    def addPostCmdExecListener(self, cb):
        _cancellers = [ exc.addPostCmdExecListener(cb) for exc in self.programs
                      ]
        return lambda : [ fn() for fn in _cancellers ]