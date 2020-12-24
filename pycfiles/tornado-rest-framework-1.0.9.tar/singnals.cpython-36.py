# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/work/lib/pyenv/versions/3.6.1/envs/maestro/lib/python3.6/site-packages/rest_framework/core/singnals.py
# Compiled at: 2018-10-12 04:41:52
# Size of source mod 2**32: 1160 bytes
import asyncio
from weakref import WeakValueDictionary
import blinker

class Signal(blinker.Signal):

    def send(self, *sender, **kwargs):
        ret = []
        for receiver, value in (super().send)(*sender, **kwargs):
            if asyncio.iscoroutinefunction(receiver):
                value = asyncio.ensure_future(value)
            ret.append((receiver, value))

        return ret


class NamedSignal(Signal):

    def __init__(self, name, doc=None):
        super().__init__(doc)
        self.name = name

    def __repr__(self):
        base = super().__repr__()
        return '%s; %r>' % (base[:-1], self.name)


class Namespace(dict):

    def signal(self, name, doc=None):
        try:
            return self[name]
        except KeyError:
            return self.setdefault(name, NamedSignal(name, doc))


class WeakNamespace(WeakValueDictionary):

    def signal(self, name, doc=None):
        try:
            return self[name]
        except KeyError:
            return self.setdefault(name, NamedSignal(name, doc))


signal = Namespace().signal
app_closed = signal('app-closed')
app_started = signal('app-started')