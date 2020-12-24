# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pytwig/bw_device.py
# Compiled at: 2020-02-17 04:01:51
# Size of source mod 2**32: 1328 bytes
from collections import OrderedDict
from pytwig.src.lib.util import *
from pytwig import bw_object, bw_atom, bw_panel

class Contents(bw_object.BW_Object):

    def add_atom(self, field, obj):
        if isinstance(obj, int):
            child = bw_atom.Atom(obj)
        else:
            if isinstance(obj, bw_atom.Atom):
                child = obj
            else:
                raise TypeError('adding something thats not an atom')
        if isinstance(self.get(field), list):
            self.get(field).append(child)
        else:
            self.set(field, child)
        return child

    def add_child(self, obj):
        if isinstance(obj, bw_atom.Atom):
            return self.add_atom(173, obj)
        if isinstance(obj, list):
            for i in obj:
                self.add_atom(173, i)
            else:
                return

    def add_panel(self, classnum):
        panel = bw_panel.Panel(classnum)
        self.get(6213).append(panel)
        return panel

    def add_proxy(self, obj, dir='out'):
        if isinstance(obj, int):
            if obj not in (50, 154):
                raise TypeError()
            proxy = bw_atom.Proxy_Port(obj)
        else:
            if isinstance(obj, bw_atom.Atom):
                proxy = obj
            elif dir == 'in':
                self.get(177).append(proxy)
            else:
                if dir == 'out':
                    self.get(178).append(proxy)
            return proxy