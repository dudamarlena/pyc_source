# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prologic/work/mio/mio/types/bytes.py
# Compiled at: 2013-12-08 17:19:04
from mio import runtime
from mio.utils import method
from mio.object import Object
from mio.lexer import encoding
from mio.core.message import Message

class Bytes(Object):

    def __init__(self, value=''):
        super(Bytes, self).__init__(value=value)
        self.create_methods()
        self.parent = runtime.find('Object')

    def __iter__(self):
        for c in self.value:
            yield self.clone(c)

    def __add__(self, other):
        return self.value + other

    def __mul__(self, other):
        return self.value * other

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __repr__(self):
        return ('b"{0:s}"').format(self.value)

    def __str__(self):
        return self.value

    def __unicode__(self):
        return self.value.decode(encoding)

    @method()
    def init(self, receiver, context, m, value=None):
        receiver.value = value or ''

    @method('__getitem__')
    def getItem(self, receiver, context, m, i):
        i = int(i.eval(context))
        return receiver.value[i]

    @method('__len__')
    def getLen(self, receiver, context, m):
        return runtime.find('Number').clone(len(receiver.value))

    @method('+')
    def add(self, receiver, context, m, other):
        return self.clone(receiver + bytes(other.eval(context)))

    @method('*')
    def mul(self, receiver, context, m, other):
        return self.clone(receiver * int(other.eval(context)))

    @method()
    def find(self, receiver, context, m, sub, start=None, end=None):
        sub = bytes(sub.eval(context))
        start = int(start.eval(context)) if start is not None else None
        end = int(end.eval(context)) if end is not None else None
        return runtime.find('Number').clone(receiver.value.find(sub, start, end))

    @method()
    def join(self, receiver, context, m, iterable):
        iterable = runtime.state.frommio(iterable.eval(context))
        return receiver.clone(receiver.value.join(iterable))

    @method()
    def lower(self, receiver, context, m):
        return self.clone(receiver.value.lower())

    @method()
    def upper(self, receiver, context, m):
        return self.clone(receiver.value.upper())