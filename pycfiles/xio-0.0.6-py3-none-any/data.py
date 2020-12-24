# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /apps/xio/core/lib/data/data.py
# Compiled at: 2018-12-07 08:05:33
import collections
from collections import OrderedDict
from pprint import pprint

def extractItems(data, filter):
    for row in data:
        if filter:
            ok = [ row[k] == v for k, v in filter.items() ]
            if all(ok):
                yield row
        else:
            yield row


def extractFields(data, fields):
    if not fields:
        return data
    import collections
    fields = [ f.strip() for f in fields.split(',') ] if not isinstance(fields, list) else fields
    out = collections.OrderedDict()
    for field in fields:
        if '.' not in field and field in data:
            out[field] = data[field]
        else:
            p = field.split('.')
            c = out
            while p and p[0] in data:
                name = p.pop(0)
                data = data.get(name, {})
                c[name] = data
                if p:
                    c[name] = c = collections.OrderedDict()

    return out


def data(src, **kwargs):
    if isinstance(src, dict):
        item = Item(src)
        if kwargs:
            return item.adapt(**kwargs)
        return item
    if isinstance(src, collections.Iterable):
        container = Container(src)
        if kwargs:
            return container.adapt(**kwargs)
        return container
    return src


class Item(dict):

    def __init__(self, *args, **kwargs):
        super(Item, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def adapt(self, fields=None):
        return extractFields(self, fields)


class Container:

    def __init__(self, data):
        self.data = data

    def adapt(self, filter=None, fields=None):
        for row in extractItems(self.data, filter):
            yield extractFields(row, fields)


class jsonld(OrderedDict):

    def __init__(self, type, context=None, **data):
        OrderedDict.__init__(self)
        if context:
            self['@context'] = context
        self['@type'] = type
        if data:
            OrderedDict.update(self, data)

    def update(self, data):
        OrderedDict.update(self, data)
        return self


class jsonldlist(jsonld):

    def __init__(self, context=None):
        jsonld.__init__(self, 'ItemList', context=context)
        self['numberOfItems'] = 0
        self['itemListElement'] = []

    def append(self, item):
        self['itemListElement'].append(item)
        self['numberOfItems'] += 1