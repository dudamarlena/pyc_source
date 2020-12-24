# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/ordereddict.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 4094 bytes
from UserDict import DictMixin

class OrderedDict(dict, DictMixin):

    def __init__(self, *args, **kwds):
        if len(args) > 1:
            raise TypeError('expected at most 1 arguments, got %d' % len(args))
        try:
            self._OrderedDict__end
        except AttributeError:
            self.clear()

        (self.update)(*args, **kwds)

    def clear(self):
        self._OrderedDict__end = end = []
        end += [None, end, end]
        self._OrderedDict__map = {}
        dict.clear(self)

    def __setitem__(self, key, value):
        if key not in self:
            end = self._OrderedDict__end
            curr = end[1]
            curr[2] = end[1] = self._OrderedDict__map[key] = [key, curr, end]
        dict.__setitem__(self, key, value)

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        key, prev, next = self._OrderedDict__map.pop(key)
        prev[2] = next
        next[1] = prev

    def __iter__(self):
        end = self._OrderedDict__end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self._OrderedDict__end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def popitem(self, last=True):
        if not self:
            raise KeyError('dictionary is empty')
        elif last:
            key = reversed(self).next()
        else:
            key = iter(self).next()
        value = self.pop(key)
        return (key, value)

    def __reduce__(self):
        items = [[k, self[k]] for k in self]
        tmp = (self._OrderedDict__map, self._OrderedDict__end)
        del self._OrderedDict__map
        del self._OrderedDict__end
        inst_dict = vars(self).copy()
        self._OrderedDict__map, self._OrderedDict__end = tmp
        if inst_dict:
            return (
             self.__class__, (items,), inst_dict)
        return (
         self.__class__, (items,))

    def keys(self):
        return list(self)

    setdefault = DictMixin.setdefault
    update = DictMixin.update
    pop = DictMixin.pop
    values = DictMixin.values
    items = DictMixin.items
    iterkeys = DictMixin.iterkeys
    itervalues = DictMixin.itervalues
    iteritems = DictMixin.iteritems

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, self.items())

    def copy(self):
        return self.__class__(self)

    @classmethod
    def fromkeys(cls, iterable, value=None):
        d = cls()
        for key in iterable:
            d[key] = value

        return d

    def __eq__(self, other):
        if isinstance(other, OrderedDict):
            if len(self) != len(other):
                return False
            for p, q in zip(self.items(), other.items()):
                if p != q:
                    return False

            return True
        return dict.__eq__(self, other)

    def __ne__(self, other):
        return not self == other