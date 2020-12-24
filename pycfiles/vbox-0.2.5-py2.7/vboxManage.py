# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\vbox\cli\vboxManage.py
# Compiled at: 2013-03-15 12:05:06
from . import chgCmds, infoCmds, base
from .list import List

class VBoxManage(base.CliVirtualBoxElement):
    """Python representation of VboxManage executable."""
    _cliAccessor = None

    def __init__(self, parent, executable='VBoxManage'):
        super(VBoxManage, self).__init__(parent)
        self._cliAccessor = _cli = base.Command(self, executable)
        _parts = {'controlvm': chgCmds.ControlVm(_cli), 
           'createhd': chgCmds.CreateHD(_cli), 
           'createvm': chgCmds.CreateVM(_cli), 
           'list': List(_cli), 
           'showhdinfo': infoCmds.ShowHdInfo(_cli), 
           'showvminfo': infoCmds.ShowVmInfo(_cli), 
           'startvm': chgCmds.StartVm(_cli), 
           'storageattach': chgCmds.StorageAttach(_cli), 
           'storagectl': chgCmds.StorageCtl(_cli), 
           'unregistervm': chgCmds.UnregisterVM(_cli), 
           'modifyvm': chgCmds.ModifyVm(_cli), 
           'clonevm': chgCmds.CloneVM(_cli), 
           'clonehd': chgCmds.CloneHd(_cli)}
        for name, obj in _parts.iteritems():
            setattr(self, name, obj)

        self._executables = tuple(_parts.values())

    def addPreCmdExecListener(self, cb):
        _cancellers = [ el.addPreCmdExecListener(cb) for el in self._executables
                      ]
        return lambda : [ fn() for fn in _cancellers ]

    def addPostCmdExecListener(self, cb):
        _cancellers = [ el.addPostCmdExecListener(cb) for el in self._executables
                      ]
        return lambda : [ fn() for fn in _cancellers ]