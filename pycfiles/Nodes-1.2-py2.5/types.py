# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/nodes/stacker/types.py
# Compiled at: 2009-06-08 07:08:42


class ConcreteType(object):
    __slots__ = ('type', )

    def __new__(cls, type):
        if isinstance(type, ConcreteType):
            type = type.type
        if type is NullType or type is None:
            return NullType
        self = object.__new__(cls)
        self.type = type
        return self

    def __eq__(self, other):
        if isinstance(other, ConcreteType):
            other = other.type
        theself = self.type
        if theself != '' and other != '':
            return theself == other
        return True

    def __nonzero__(self):
        return self.type != ''


def product(l1, l2):
    return ((a, b) for a in l1 for b in l2)


from operator import attrgetter
bytype = attrgetter('type')

class Type(object):
    __slots__ = ('types', )

    def __new__(cls, types):
        if types is None or types is NullType:
            return NullType
        self = object.__new__(cls)
        if isinstance(types, ConcreteType):
            self.types = [
             types]
            return self
        if isinstance(types, Type):
            self.types = types.types
            return self
        if isinstance(types, basestring):
            types = types.split()
        types = [ ConcreteType(type) for type in types ]
        types = [ type for type in types if type is not NullType ]
        types.sort(key=bytype)
        self.types = types
        return self

    def __eq__(self, other):
        if not isinstance(other, Type):
            other = Type(other)
        if not (self and other):
            return True
        theself = iter(self.types)
        theother = iter(other.types)
        a = theself.next()
        b = theother.next()
        try:
            while 1:
                if a.type < b.type:
                    a = theself.next()
                elif a.type > b.type:
                    b = theother.next()
                elif a.type == b.type:
                    break
                else:
                    raise ValueError, 'fatal eroor: incomparable'

            return True
        except StopIteration:
            return False

    def __ne__(self, other):
        return not self == other

    def __len__(self):
        return len(self.types)

    def __and__(self, other):
        other = Type(other)
        if not self:
            return Type(other)
        if not other:
            return Type(self)
        theself = iter(self.types)
        theother = iter(other.types)
        isect = []
        a = theself.next()
        b = theother.next()
        try:
            while 1:
                if a == b:
                    isect.append(a)
                    a = theself.next()
                    b = theother.next()
                    continue
                if a.type < b.type:
                    a = theself.next()
                elif a.type > b.type:
                    b = theother.next()

        except StopIteration:
            pass

        return Type(isect) if isect else NullType


class NullTypeT(object):
    __slots__ = ()

    def __new__(cls):
        raise ValueError, 'NullType could not be created'

    def __eq__(self, other):
        return False

    def __ne__(self, other):
        return True

    def __nonzero__(self):
        return False

    def __len__(self):
        return 0

    def __and__(self, other):
        return self

    def __rand__(self, other):
        return self


NullType = object.__new__(NullTypeT)
del NullTypeT