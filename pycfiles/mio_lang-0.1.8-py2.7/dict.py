# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prologic/work/mio/mio/types/dict.py
# Compiled at: 2013-12-08 17:19:04
from mio import runtime
from mio.utils import method
from mio.object import Object
from mio.errors import KeyError

class Dict(Object):

    def __init__(self, value={}):
        super(Dict, self).__init__(value=value)
        self.create_methods()
        self.parent = runtime.find('Object')

    def __hash__(self):
        return

    def __len__(self):
        return len(self.value)

    def __iter__(self):
        if isinstance(self.value, dict):
            return iter(self.value)
        return iter({})

    def __repr__(self):
        return repr(self.value)

    @method()
    def init(self, receiver, context, m, iterable=None):
        if isinstance(iterable, Dict):
            receiver.value = iterable.value.copy()
        else:
            receiver.value = dict(iterable) if iterable is not None else dict()
        return receiver

    @method('__len__')
    def getLen(self, receiver, context, m):
        return runtime.find('Number').clone(len(receiver.value))

    @method('__getitem__')
    def getitem(self, receiver, context, m, key):
        key = key.eval(context)
        if key in receiver.value:
            return receiver.value[key]
        raise KeyError(unicode(key))

    @method('__setitem__')
    def setitem(self, receiver, context, m, key, value):
        receiver.value[key.eval(context)] = value.eval(context)
        return receiver

    @method('__delitem__')
    def delitem(self, receiver, context, m, key):
        del receiver.value[key.eval(context)]
        return receiver

    @method(property=True)
    def keys(self, receiver, context, m):
        return runtime.find('List').clone(receiver.value.keys())

    @method(property=True)
    def items(self, receiver, context, m):
        List = runtime.find('List')
        items = [ List.clone([k, v]) for k, v in receiver.value.items() ]
        return runtime.find('List').clone(items)

    @method(property=True)
    def values(self, receiver, context, m):
        return runtime.find('List').clone(receiver.value.values())

    @method(property=True)
    def len(self, receiver, context, m):
        return runtime.find('Number').clone(len(receiver.value))