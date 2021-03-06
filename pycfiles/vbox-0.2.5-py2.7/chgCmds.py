# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\vbox\cli\chgCmds.py
# Compiled at: 2013-03-15 12:05:06
"""Commands that alter virtualbox states."""
from .subCmd import CmdError, Generic, PlainCall, ArgCmd
from . import util

class CreateHD(Generic):
    changesVmState = True
    opts = ('filename', 'size', 'format', 'variant')
    mandatory = ('filename', 'size')

    def getRcHandlers(self):
        return {0: self._findErrors}

    def _findErrors(self, cmd, output):
        txt = output.lower()
        if 'error:' in txt or 'verr_' in txt:
            raise CmdError(cmd, 0, output)
        elif not txt:
            raise Exception('Expected for `createhd` to write something to the output.')
        return output


class CreateVM(Generic):
    changesVmState = True
    opts = ('name', 'groups', 'ostype', 'basefolder', 'uuid')
    flags = ('register', )
    mandatory = ('name', )


class CloneVM(ArgCmd):
    changesVmState = False
    opts = ('snapshot', 'mode', 'options', 'name', 'groups', 'basefolder', 'uuid')
    flags = ('register', )


class CloneHd(ArgCmd):
    changesVmState = False
    nargs = 2
    opts = ('outputfile', 'format', 'variant')
    flags = ('existing', )


class UnregisterVM(ArgCmd):
    changesVmState = True
    flags = ('delete', )


class StorageCtl(ArgCmd):
    nargs = 2
    argnames = (None, '--name')
    changesVmState = True
    opts = ('add', 'controller', 'sataportcount')
    bools = ('hostiocache', 'bootable')
    flags = 'remove'


class StorageAttach(ArgCmd):
    changesVmState = True
    nargs = 2
    argnames = (None, '--storagectl')
    changesVmState = True
    opts = ('port', 'device', 'type', 'medium')
    mandatory = ('type', )


class StartVm(ArgCmd):
    """Start VM."""
    changesVmState = True
    opts = ('type', )


class ControlVm(ArgCmd):
    changesVmState = True

    def __call__(self, name, action):
        return self.checkOutput([name, action])

    def pause(self, name):
        return self(name, 'pause')

    def resume(self, name):
        return self(name, 'resume')

    def reset(self, name):
        return self(name, 'reset')

    def poweroff(self, name):
        return self(name, 'poweroff')

    def savestate(self, name):
        return self(name, 'savestate')


class ModifyVm(PlainCall):
    """ModifyVm bindings."""
    changesVmState = True