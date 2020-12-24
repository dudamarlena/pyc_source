# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\pyDots\nones.py
# Compiled at: 2016-12-30 16:05:06
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
from pyDots import split_field, _setdefault, wrap
_get = object.__getattribute__
_set = object.__setattr__
_zero_list = []

class NullType(object):
    """
    Structural Null provides closure under the dot (.) operator
        Null[x] == Null
        Null.x == Null

    Null INSTANCES WILL TRACK THEIR OWN DEREFERENCE PATH SO
    ASSIGNMENT CAN BE DONE
    """

    def __init__(self, obj=None, key=None):
        """
        obj - VALUE BEING DEREFERENCED
        key - THE dict ITEM REFERENCE (DOT(.) IS NOT ESCAPED)
        """
        d = _get(self, b'__dict__')
        d[b'_obj'] = obj
        d[b'__key__'] = key

    def __bool__(self):
        return False

    def __nonzero__(self):
        return False

    def __add__(self, other):
        if isinstance(other, list):
            return other
        return Null

    def __radd__(self, other):
        return Null

    def __call__(self, *args, **kwargs):
        return Null

    def __iadd__(self, other):
        try:
            d = _get(self, b'__dict__')
            o = d[b'_obj']
            if o is None:
                return self
            key = d[b'__key__']
            _assign_to_null(o, [key], other)
        except Exception as e:
            raise e

        return other

    def __sub__(self, other):
        return Null

    def __rsub__(self, other):
        return Null

    def __neg__(self):
        return Null

    def __mul__(self, other):
        return Null

    def __rmul__(self, other):
        return Null

    def __div__(self, other):
        return Null

    def __rdiv__(self, other):
        return Null

    def __truediv__(self, other):
        return Null

    def __rtruediv__(self, other):
        return Null

    def __gt__(self, other):
        return False

    def __ge__(self, other):
        return False

    def __le__(self, other):
        return False

    def __lt__(self, other):
        return False

    def __eq__(self, other):
        return other == None or isinstance(other, NullType)

    def __ne__(self, other):
        return other is not None and not isinstance(other, NullType)

    def __or__(self, other):
        if other is True:
            return True
        return Null

    def __ror__(self, other):
        return other

    def __and__(self, other):
        if other is False:
            return False
        return Null

    def __xor__(self, other):
        return Null

    def __len__(self):
        return 0

    def __iter__(self):
        return _zero_list.__iter__()

    def __deepcopy__(self, memo):
        return

    def last(self):
        """
        IN CASE self IS INTERPRETED AS A list
        """
        return Null

    def right(self, num=None):
        return Null

    def __getitem__(self, key):
        assert not isinstance(key, str)
        if isinstance(key, slice):
            return Null
        if isinstance(key, str):
            key = key.decode(b'utf8')
        elif isinstance(key, int):
            return NullType(self, key)
        path = split_field(key)
        output = self
        for p in path:
            output = NullType(output, p)

        return output

    def __getattribute__(self, key):
        if key == b'__class__':
            return NullType
        else:
            key = key.decode(b'utf8')
            d = _get(self, b'__dict__')
            o = wrap(d[b'_obj'])
            k = d[b'__key__']
            if o is None:
                return Null
            if isinstance(o, NullType):
                return NullType(self, key)
            v = o.get(k)
            if v == None:
                return NullType(self, key)
            return wrap(v).get(key)

    def __setattr__(self, key, value):
        key = key.decode(b'utf8')
        d = _get(self, b'__dict__')
        o = wrap(d[b'_obj'])
        k = d[b'__key__']
        seq = [
         k] + [key]
        _assign_to_null(o, seq, value)

    def __setitem__(self, key, value):
        assert not isinstance(key, str)
        d = _get(self, b'__dict__')
        o = d[b'_obj']
        k = d[b'__key__']
        seq = [
         k] + split_field(key)
        _assign_to_null(o, seq, value)

    def keys(self):
        return set()

    def items(self):
        return []

    def pop(self, key, default=None):
        return Null

    def __str__(self):
        return b'None'

    def __repr__(self):
        return b'Null'

    def __hash__(self):
        return hash(None)


Null = NullType()

def _assign_to_null(obj, path, value, force=True):
    """
    value IS ASSIGNED TO obj[self.path][key]
    path IS AN ARRAY OF PROPERTY NAMES
    force=False IF YOU PREFER TO use setDefault()
    """
    if isinstance(obj, NullType):
        d = _get(obj, b'__dict__')
        o = d[b'_obj']
        p = d[b'__key__']
        s = [p] + path
        return _assign_to_null(o, s, value)
    else:
        path0 = path[0]
        if len(path) == 1:
            if force:
                obj[path0] = value
            else:
                _setdefault(obj, path0, value)
            return
        old_value = obj.get(path0)
        if old_value == None:
            if value == None:
                return
            obj[path0] = old_value = {}
        _assign_to_null(old_value, path[1:], value)
        return