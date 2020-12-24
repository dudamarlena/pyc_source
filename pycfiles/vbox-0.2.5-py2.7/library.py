# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\vbox\vm\library.py
# Compiled at: 2013-03-15 12:05:06
import re
from . import base, vm

class VmLibrary(base.VirtualBoxEntityType):
    cls = vm.VM

    def _nameGen(self, basename, autoname):
        if basename:
            name = basename
        else:
            name = 'unnamed_machine'
        existing = [ vm.name for vm in self.list() ]
        if name not in existing:
            yield name
        if not autoname:
            raise Exception(('Virtual machine {!r} already exists.').format(name))
        idx = 1
        genName = lambda : ('{} ({})').format(name, idx)
        while genName() in existing:
            idx += 1

        while True:
            yield genName()
            idx += 1

    def create(self, autoname=True, ostype=None, **kwargs):
        super(VmLibrary, self).create()
        name = kwargs.pop('name', None)
        if ostype:
            found = self.vb.info.ostypes.find(ostype)
            if not found:
                raise Exception(('OS type {!r} not found').format(ostype))
            kwargs['ostype'] = found.id
        nameGen = self._nameGen(name, autoname)
        while True:
            kwargs['name'] = nameGen.next()
            try:
                out = self.vb.cli.manage.createvm(**kwargs)
            except cli.CmdError as err:
                if 'already exists' in err.output.lower():
                    continue
                else:
                    raise
            else:
                break

        out = self.cli.util.parseParams(out)
        return self.get(out['Settings file'])

    cloneMsgRe = re.compile('^Machine has been successfully cloned as "(.*)"\\s*$', re.I | re.M)

    def clone(self, source, autoname=True, **kwargs):
        if 'name' in kwargs:
            gen = self._nameGen(kwargs['name'], autoname)
            kwargs['name'] = gen.next()
        out = self.vb.cli.manage.clonevm(source, **kwargs)
        match = self.cloneMsgRe.search(out)
        assert match, repr(out)
        machineName = match.group(1)
        return self.get(machineName)

    def listRegisteredIds(self):
        return self.vb.cli.manage.list.vms().values()