# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prologic/work/mio/mio/types/tuple.py
# Compiled at: 2013-11-18 07:11:47
from mio import runtime
from mio.utils import method
from mio.object import Object

class Tuple(Object):

    def __init__(self, value=()):
        super(Tuple, self).__init__(value=value)
        self.create_methods()
        self.parent = runtime.find('Object')

    def __len__(self):
        return len(self.value)

    def __iter__(self):
        if isinstance(self.value, tuple):
            return iter(self.value)
        return iter(())

    def __repr__(self):
        return repr(self.value)

    @method()
    def init(self, receiver, context, m, iterable=None):
        receiver.value = tuple(iterable) if iterable is not None else tuple()
        return receiver

    @method('__getitem__')
    def getItem(self, receiver, context, m, i):
        i = int(i.eval(context))
        return receiver.value[i]

    @method('__len__')
    def getLen(self, receiver, context, m):
        return runtime.find('Number').clone(len(receiver.value))

    @method()
    def count(self, receiver, context, m, value):
        return runtime.find('Number').clone(receiver.value.count(value.eval(context)))

    @method(property=True)
    def len(self, receiver, context, m):
        return runtime.find('Number').clone(len(receiver.value))

    @method()
    def at(self, receiver, context, m, index):
        return receiver.value[int(index.eval(context))]

    @method()
    def reversed(self, receiver, context, m):
        return receiver.clone(tuple(reversed(receiver.value)))

    @method()
    def sorted(self, receiver, context, m):
        return receiver.clone(tuple(sorted(receiver.value)))