# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ganesh/work/silota-python/silota/structures.py
# Compiled at: 2013-11-30 15:29:50


class KeyedListResource(object):
    """docstring for ListResource"""

    def __init__(self, items=None):
        super(KeyedListResource, self).__init__()
        self._h = None
        self._items = items or list()
        self._obj = None
        self._kwargs = {}
        return

    def __repr__(self):
        return repr(self._items)

    def __iter__(self):
        for item in self._items:
            yield item

    def __len__(self):
        if hasattr(self, '_count'):
            return self._count
        return len(self._items)

    def __getitem__(self, key):
        if isinstance(key, int):
            if abs(key) <= len(self._items):
                return self._items[key]
        v = self.get(key)
        if v is None:
            raise KeyError(key)
        return v

    def add(self, *args, **kwargs):
        try:
            return self[0].new(*args, **kwargs)
        except IndexError:
            o = self._obj()
            o._h = self._h
            o.__dict__.update(self._kwargs)
            return o.new(*args, **kwargs)

    def remove(self, key):
        if hasattr(self[0], 'delete'):
            return self[key].delete()

    def get(self, key):
        for item in self:
            if key in item._ids:
                return item

    def __delitem__(self, key):
        self[key].delete()


class PagedKeyedListResource(KeyedListResource):

    def __init__(self, items=None):
        super(PagedKeyedListResource, self).__init__(items=items)