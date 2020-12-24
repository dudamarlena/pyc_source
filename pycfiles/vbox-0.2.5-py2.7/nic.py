# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\vbox\vm\nic.py
# Compiled at: 2013-03-15 12:05:06
"""Network interface card support."""
import re
from vbox import util as props
from . import base, util

class NIC(base.VirtualMachinePart):
    hwType = property(lambda s: s.getProp('nictype'))
    speed = property(lambda s: int(s.getProp('nicspeed')))

    def _getInfo(self):
        par = self.vm.info
        if not par:
            return None
        else:
            out = {}
            for name in ('nic', 'nictype', 'nicspeed', 'cableconnected', 'macaddress',
                         'bridgeadapter', 'hostonlyadapter'):
                name = self.getPropName(name)
                out[name] = par.get(name)

            return out

    def getPropName(self, prefix):
        return ('{}{}').format(prefix, self.idx)

    def type():
        doc = 'The type property.'

        def fget(self):
            rv = self.getProp('nic')
            if rv == 'none':
                rv = None
            return rv

        def fset(self, value):
            if value is None:
                value = 'none'
            self.setProp('nic', value)
            self.control({'nic': value}, quiet=True)
            if not self.networkAdapter:
                if value == 'hostonly':
                    lib = self.vb.net.hostOnlyInterfaces
                elif value == 'bridgeadapter':
                    lib = self.vb.net.bridgedInterfaces
                else:
                    lib = None
                if lib:
                    for el in lib.list():
                        adapter = el
                        break
                    else:
                        adapter = None

                if adapter:
                    self.networkAdapter = adapter
            return

        def fdel(self):
            self.type = None
            return

        return locals()

    type = property(**type())
    cableConnected = props.Switch('cableconnected', extraCb=util.controlCb('setlinkstate'))
    mac = props.String('macaddress')

    def networkAdapter():
        doc = 'The networkAdapter property.\n\n        Controls acutal host-level NIC attached to the VM nic\n        '

        def _propName(typ):
            if typ == 'hostonly':
                rv = 'hostonlyadapter'
            elif typ == 'bridged':
                rv = 'bridgeadapter'
            else:
                rv = None
            return rv

        def fget(self):
            prop = _propName(self.type)
            if not prop:
                return
            else:
                adapterName = self.getProp(prop)
                if adapterName:
                    rv = self.vb.net.find(adapterName)
                    assert rv
                else:
                    rv = None
                return rv

        def fset(self, value):
            prop = _propName(self.type)
            if not prop:
                return
            else:
                if not value:
                    value = None
                else:
                    try:
                        value = value.name
                    except AttributeError:
                        value = str(value)

                self.setProp(prop, value)
                return

        return {'fget': fget, 'fset': fset}

    networkAdapter = property(**networkAdapter())


class NicGroup(base.PartGroup):
    parentRe = re.compile('^nic(\\d+)$')
    childCls = NIC