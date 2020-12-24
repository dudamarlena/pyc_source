# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/stuf/collects.py
# Compiled at: 2014-12-18 18:07:56
"""stuf collections."""
import sys
from .deep import getcls
from .base import second, first
from .six import OrderedDict, items
try:
    from reprlib import recursive_repr
except ImportError:
    from .six import get_ident, getdoc, getmod, docit

    def recursive_repr(fillvalue='...'):

        def decorating_function(user_function):
            repr_running = set()

            def wrapper(self):
                key = (id(self), get_ident())
                if key in repr_running:
                    return fillvalue
                repr_running.add(key)
                try:
                    result = user_function(self)
                finally:
                    repr_running.discard(key)

                return result

            wrapper.__module__ = getmod(user_function)
            docit(wrapper, getdoc(user_function))
            return wrapper

        return decorating_function


version = sys.version_info
if version[0] == 3 and version[1] > 1:
    from collections import Counter
else:
    from heapq import nlargest
    from itertools import chain, starmap, repeat
    from .deep import clsname
    from .base import ismapping

    class Counter(dict):
        """dict subclass for counting hashable items"""

        def __init__(self, iterable=None, **kw):
            """
            If given, count elements from an input iterable. Or, initialize
            count from another mapping of elements to their counts.
            """
            super(Counter, self).__init__()
            self.update(iterable, **kw)

        def __missing__(self, key):
            """The count of elements not in the Counter is zero."""
            return 0

        def __reduce__(self):
            return (
             getcls(self), (dict(self),))

        def __delitem__(self, elem):
            """
            Like dict.__delitem__() but does not raise KeyError for missing'
            values.
            """
            if elem in self:
                super(Counter, self).__delitem__(elem)

        def __repr__(self):
            if not self:
                return '%s()' % clsname(self)
            try:
                items = (', ').join(map(('%r: %r').__mod__, self.most_common()))
                return '%s({%s})' % (clsname(self), items)
            except TypeError:
                return ('{0}({1!r})').format(clsname(self), dict(self))

        def __add__(self, other):
            """Add counts from two counters."""
            if not isinstance(other, getcls(self)):
                return NotImplemented()
            result = getcls(self)()
            for (elem, count) in items(self):
                newcount = count + other[elem]
                if newcount > 0:
                    result[elem] = newcount

            for (elem, count) in items(other):
                if elem not in self and count > 0:
                    result[elem] = count

            return result

        def __sub__(self, other):
            """Subtract count, but keep only results with positive counts."""
            if not isinstance(other, getcls(self)):
                return NotImplemented()
            result = getcls(self)()
            for (elem, count) in items(self):
                newcount = count - other[elem]
                if newcount > 0:
                    result[elem] = newcount

            for (elem, count) in items(other):
                if elem not in self and count < 0:
                    result[elem] = 0 - count

            return result

        def __or__(self, other):
            """Union is the maximum of value in either of the input counters."""
            if not isinstance(other, getcls(self)):
                return NotImplemented()
            result = getcls(self)()
            for (elem, count) in items(self):
                other_count = other[elem]
                newcount = other_count if count < other_count else count
                if newcount > 0:
                    result[elem] = newcount

            for (elem, count) in items(other):
                if elem not in self and count > 0:
                    result[elem] = count

            return result

        def __and__(self, other):
            """Intersection is the minimum of corresponding counts."""
            if not isinstance(other, getcls(self)):
                return NotImplemented()
            result = getcls(self)()
            for (elem, count) in items(self):
                other_count = other[elem]
                newcount = count if count < other_count else other_count
                if newcount > 0:
                    result[elem] = newcount

            return result

        def __pos__(self):
            """
            Adds an empty counter, effectively stripping negative and zero
            counts.
            """
            return self + getcls(self)()

        def __neg__(self):
            """
            Subtracts from an empty counter. Strips positive and zero counts,
            and flips the sign on negative counts.
            """
            return getcls(self)() - self

        def most_common(self, n=None, nl=nlargest, i=items, g=second):
            """
            List the n most common elements and their counts from the most
            common to the least. If n is None, then list all element counts.
            """
            if n is None:
                return sorted(i(self), key=g, reverse=True)
            else:
                return nl(n, i(self), key=g)

        def elements(self):
            """
            Iterator over elements repeating each as many times as its count.
            """
            return chain.from_iterable(starmap(repeat, items(self)))

        @classmethod
        def fromkeys(cls, iterable, v=None):
            raise NotImplementedError('Counter.fromkeys() undefined. Use Counter(iterable) instead.')

        def update--- This code section failed: ---

 L. 172         0  LOAD_FAST             1  'iterable'
                3  LOAD_CONST               None
                6  COMPARE_OP            9  is-not
                9  JUMP_IF_FALSE       164  'to 176'
             12_0  THEN                     177
               12  POP_TOP          

 L. 173        13  LOAD_GLOBAL           1  'ismapping'
               16  LOAD_FAST             1  'iterable'
               19  CALL_FUNCTION_1       1  None
               22  JUMP_IF_FALSE        98  'to 123'
             25_0  THEN                     173
               25  POP_TOP          

 L. 174        26  LOAD_FAST             0  'self'
               29  JUMP_IF_FALSE        65  'to 97'
               32  POP_TOP          

 L. 175        33  LOAD_FAST             0  'self'
               36  LOAD_ATTR             2  'get'
               39  STORE_FAST            3  'self_get'

 L. 176        42  SETUP_LOOP           75  'to 120'
               45  LOAD_GLOBAL           3  'items'
               48  LOAD_FAST             1  'iterable'
               51  CALL_FUNCTION_1       1  None
               54  GET_ITER         
               55  FOR_ITER             35  'to 93'
               58  UNPACK_SEQUENCE_2     2 
               61  STORE_FAST            4  'elem'
               64  STORE_FAST            5  'count'

 L. 177        67  LOAD_FAST             5  'count'
               70  LOAD_FAST             3  'self_get'
               73  LOAD_FAST             4  'elem'
               76  LOAD_CONST               0
               79  CALL_FUNCTION_2       2  None
               82  BINARY_ADD       
               83  LOAD_FAST             0  'self'
               86  LOAD_FAST             4  'elem'
               89  STORE_SUBSCR     
               90  JUMP_BACK            55  'to 55'
               93  POP_BLOCK        
               94  JUMP_ABSOLUTE       173  'to 173'
             97_0  COME_FROM            29  '29'
               97  POP_TOP          

 L. 179        98  LOAD_GLOBAL           4  'super'
              101  LOAD_GLOBAL           5  'Counter'
              104  LOAD_FAST             0  'self'
              107  CALL_FUNCTION_2       2  None
              110  LOAD_ATTR             6  'update'
              113  LOAD_FAST             1  'iterable'
              116  CALL_FUNCTION_1       1  None
              119  POP_TOP          
            120_0  COME_FROM            42  '42'
              120  JUMP_ABSOLUTE       177  'to 177'
            123_0  COME_FROM            22  '22'
              123  POP_TOP          

 L. 181       124  LOAD_FAST             0  'self'
              127  LOAD_ATTR             2  'get'
              130  STORE_FAST            6  'mapping_get'

 L. 182       133  SETUP_LOOP           41  'to 177'
              136  LOAD_FAST             1  'iterable'
              139  GET_ITER         
              140  FOR_ITER             29  'to 172'
              143  STORE_FAST            4  'elem'

 L. 183       146  LOAD_FAST             6  'mapping_get'
              149  LOAD_FAST             4  'elem'
              152  LOAD_CONST               0
              155  CALL_FUNCTION_2       2  None
              158  LOAD_CONST               1
              161  BINARY_ADD       
              162  LOAD_FAST             0  'self'
              165  LOAD_FAST             4  'elem'
              168  STORE_SUBSCR     
              169  JUMP_BACK           140  'to 140'
              172  POP_BLOCK        
              173  JUMP_FORWARD          1  'to 177'
            176_0  COME_FROM             9  '9'
              176  POP_TOP          
            177_0  COME_FROM           133  '133'

 L. 184       177  LOAD_FAST             2  'kwds'
              180  JUMP_IF_FALSE        17  'to 200'
            183_0  THEN                     201
              183  POP_TOP          

 L. 185       184  LOAD_FAST             0  'self'
              187  LOAD_ATTR             6  'update'
              190  LOAD_FAST             2  'kwds'
              193  CALL_FUNCTION_1       1  None
              196  POP_TOP          
              197  JUMP_FORWARD          1  'to 201'
            200_0  COME_FROM           180  '180'
              200  POP_TOP          
            201_0  COME_FROM           197  '197'
              201  LOAD_CONST               None
              204  RETURN_VALUE     

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 120

        def subtract(self, iterable=None, **kwds):
            """
            Like dict.update() but subtracts counts instead of replacing them.
            Counts can be reduced below zero.  Both the inputs and outputs are
            allowed to contain zero and negative counts.

            Source can be an iterable, a dictionary, or another Counter
            instance.
            """
            if iterable is not None:
                self_get = self.get
                if ismapping(iterable):
                    for (elem, count) in items(iterable):
                        self[elem] = self_get(elem, 0) - count

                else:
                    for elem in iterable:
                        self[elem] = self_get(elem, 0) - 1

            if kwds:
                self.subtract(kwds)
            return

        def copy(self):
            """Return a shallow copy."""
            return getcls(self)(self)


try:
    from collections import ChainMap
except ImportError:
    from collections import MutableMapping

    class ChainMap(MutableMapping):
        """
        `ChainMap` groups multiple dicts (or other mappings) together to create
        a single, updateable view.
        """

        def __init__(self, *maps):
            """
            Initialize `ChainMap` by setting *maps* to the given mappings. If no
            mappings are provided, a single empty dictionary is used.
            """
            self.maps = list(maps) or [OrderedDict()]

        def __missing__(self, key):
            raise KeyError(key)

        def __getitem__(self, key):
            for mapping in self.maps:
                try:
                    return mapping[key]
                except KeyError:
                    pass

            return self.__missing__(key)

        def get(self, key, default=None):
            if key in self:
                return self[key]
            return default

        def __len__(self):
            return len(set().union(*self.maps))

        def __iter__(self, set=set):
            return set().union(*self.maps).__iter__()

        def __contains__(self, key, any=any):
            return any(key in m for m in self.maps)

        def __bool__(self, any=any):
            return any(self.maps)

        @classmethod
        def fromkeys(cls, iterable, *args):
            """
            Create a ChainMap with a single dict created from the iterable.
            """
            return cls(dict.fromkeys(iterable, *args))

        def copy(self):
            """
            New ChainMap or subclass with a new copy of maps[0] and refs to
            maps[1:]
            """
            return getcls(self)(first(self.maps).copy(), *self.maps[1:])

        __copy__ = copy

        def new_child(self):
            """New ChainMap with a new dict followed by all previous maps."""
            return getcls(self)({}, *self.maps)

        @property
        def parents(self):
            """New ChainMap from maps[1:]."""
            return getcls(self)(*self.maps[1:])

        def __setitem__(self, key, value):
            first(self.maps)[key] = value

        def __delitem__(self, key):
            try:
                del first(self.maps)[key]
            except KeyError:
                raise KeyError(('Key not found in the first mapping: {r}').format(key))

        def popitem(self):
            """
            Remove and return an item pair from maps[0]. Raise `KeyError` is
            maps[0] is empty.
            """
            try:
                return first(self.maps).popitem()
            except KeyError:
                raise KeyError('No keys found in the first mapping.')

        def pop(self, key, *args):
            """
            Remove *key* from maps[0] and return its value. Raise KeyError if
            *key* not in maps[0].
            """
            try:
                return first(self.maps).pop(key, *args)
            except KeyError:
                raise KeyError(('Key not found in the first mapping: {r}').format(key))

        def clear(self):
            """Clear maps[0], leaving maps[1:] intact."""
            first(self.maps).clear()