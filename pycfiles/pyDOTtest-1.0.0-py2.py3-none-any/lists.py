# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\pyDots\lists.py
# Compiled at: 2017-01-16 16:07:47
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
from copy import deepcopy
from pyDots import wrap, unwrap, coalesce
from pyDots.nones import Null
_get = object.__getattribute__
_set = object.__setattr__
_emit_slice_warning = True
_datawrap = None

def _late_import():
    global _datawrap
    from pyDots.objects import datawrap as _datawrap
    _ = _datawrap


class FlatList(list):
    """
    ENCAPSULATES HANDING OF Nulls BY wrapING ALL MEMBERS AS NEEDED
    ENCAPSULATES FLAT SLICES ([::]) FOR USE IN WINDOW FUNCTIONS
    """
    EMPTY = None

    def __init__(self, vals=None):
        """ USE THE vals, NOT A COPY """
        if vals == None:
            self.list = []
        elif isinstance(vals, FlatList):
            self.list = vals.list
        else:
            self.list = vals
        return

    def __getitem__(self, index):
        if isinstance(index, slice):
            if index.step is not None:
                if not _Log:
                    _late_import()
                _Log.error(b'slice step must be None, do not know how to deal with values')
            length = len(_get(self, b'list'))
            i = index.start
            i = min(max(i, 0), length)
            j = index.stop
            if j is None:
                j = length
            else:
                j = max(min(j, length), 0)
            return FlatList(_get(self, b'list')[i:j])
        else:
            if index < 0 or len(_get(self, b'list')) <= index:
                return Null
            return wrap(_get(self, b'list')[index])

    def __setitem__(self, i, y):
        try:
            _list = _get(self, b'list')
            if i <= len(_list):
                for i in range(len(_list), i):
                    _list.append(None)

            _list[i] = unwrap(y)
        except Exception as e:
            if not _datawrap:
                _late_import()
            _Log.error(b'problem', cause=e)

        return

    def __getattribute__(self, key):
        try:
            if key != b'index':
                output = _get(self, key)
                return output
        except Exception as e:
            if key[0:2] == b'__':
                raise e

        return FlatList.get(self, key)

    def get(self, key):
        """
        simple `select`
        """
        if not _datawrap:
            _late_import()
        return FlatList(vals=[ unwrap(coalesce(_datawrap(v), Null)[key]) for v in _get(self, b'list') ])

    def select(self, key):
        if not _Log:
            _late_import()
        _Log.error(b'Not supported.  Use `get()`')

    def filter(self, _filter):
        return FlatList(vals=[ unwrap(u) for u in (wrap(v) for v in _get(self, b'list')) if _filter(u) ])

    def __delslice__(self, i, j):
        _Log.error(b'Can not perform del on slice: modulo arithmetic was performed on the parameters.  You can try using clear()')

    def __clear__(self):
        self.list = []

    def __iter__(self):
        return (wrap(v) for v in _get(self, b'list'))

    def __contains__(self, item):
        return list.__contains__(_get(self, b'list'), item)

    def append(self, val):
        _get(self, b'list').append(unwrap(val))
        return self

    def __str__(self):
        return _get(self, b'list').__str__()

    def __len__(self):
        return _get(self, b'list').__len__()

    def __getslice__(self, i, j):
        global _emit_slice_warning
        if _emit_slice_warning:
            _emit_slice_warning = False
            if not _Log:
                _late_import()
            _Log.warning(b'slicing is broken in Python 2.7: a[i:j] == a[i+len(a), j] sometimes.  Use [start:stop:step] (see https://github.com/klahnakoski/pyLibrary/blob/master/pyLibrary/dot/README.md#the-slice-operator-in-python27-is-inconsistent)')
        return self[i:j:]

    def __list__(self):
        return self.list

    def copy(self):
        return FlatList(list(_get(self, b'list')))

    def __copy__(self):
        return FlatList(list(_get(self, b'list')))

    def __deepcopy__(self, memo):
        d = _get(self, b'list')
        return wrap(deepcopy(d, memo))

    def remove(self, x):
        _get(self, b'list').remove(x)
        return self

    def extend(self, values):
        for v in values:
            _get(self, b'list').append(unwrap(v))

        return self

    def pop(self, index=None):
        return wrap(_get(self, b'list').pop(index))

    def __add__(self, value):
        output = list(_get(self, b'list'))
        output.extend(value)
        return FlatList(vals=output)

    def __or__(self, value):
        output = list(_get(self, b'list'))
        output.append(value)
        return FlatList(vals=output)

    def __radd__(self, other):
        output = list(other)
        output.extend(_get(self, b'list'))
        return FlatList(vals=output)

    def __iadd__(self, other):
        if isinstance(other, list):
            self.extend(other)
        else:
            self.append(other)
        return self

    def right(self, num=None):
        """
        WITH SLICES BEING FLAT, WE NEED A SIMPLE WAY TO SLICE FROM THE RIGHT [-num:]
        """
        if num == None:
            return FlatList([_get(self, b'list')[(-1)]])
        else:
            if num <= 0:
                return Null
            return FlatList(_get(self, b'list')[-num:])

    def left(self, num=None):
        """
        NOT REQUIRED, BUT EXISTS AS OPPOSITE OF right()
        """
        if num == None:
            return FlatList([_get(self, b'list')[0]])
        else:
            if num <= 0:
                return Null
            return FlatList(_get(self, b'list')[:num])

    def not_right(self, num):
        """
        WITH SLICES BEING FLAT, WE NEED A SIMPLE WAY TO SLICE FROM THE LEFT [:-num:]
        """
        if num == None:
            return FlatList([_get(self, b'list')[:-1:]])
        else:
            if num <= 0:
                return FlatList.EMPTY
            return FlatList(_get(self, b'list')[:-num:])

    def not_left(self, num):
        """
        NOT REQUIRED, EXISTS AS OPPOSITE OF not_right()
        """
        if num == None:
            return FlatList([_get(self, b'list')[(-1)]])
        else:
            if num <= 0:
                return self
            return FlatList(_get(self, b'list')[num::])

    def last(self):
        """
        RETURN LAST ELEMENT IN FlatList [-1]
        """
        lst = _get(self, b'list')
        if lst:
            return wrap(lst[(-1)])
        return Null

    def map(self, oper, includeNone=True):
        if includeNone:
            return FlatList([ oper(v) for v in _get(self, b'list') ])
        return FlatList([ oper(v) for v in _get(self, b'list') if v != None ])
        return


FlatList.EMPTY = Null