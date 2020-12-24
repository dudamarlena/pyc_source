# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\billingtonm\dropbox\code\pydiagrams\build\lib\pydiagrams\baseItems.py
# Compiled at: 2019-10-20 22:32:24
# Size of source mod 2**32: 1710 bytes
import sys
from collections import OrderedDict
module_globals = sys.modules['__main__'].__dict__

class BaseItem(object):
    __doc__ = ' Defines a base item, eg: a Component in a Component Diagram '

    def __init__(self, label, **attrs):
        self.owner = None
        self.label = label
        self.attrs = attrs
        self.id = None

    def __repr__(self):
        return 'BaseItem.label = "{}"'.format(self.label)

    @property
    def Diagram(self):
        if self.owner:
            return self.owner.diagram
        raise ValueError('%s has no owner' % self.__repr__())

    @property
    def Helper(self):
        return self.Diagram.helper


class BaseItemCollection(object):
    __doc__ = ' Represents an Object that owns base items, eg: a Diagram '

    def __init__(self, diagram):
        self.collection = OrderedDict()
        self.diagram = diagram

    def add_item(self, i):
        """ Add BaseItem i to the collection """
        i.owner = self
        self.collection[hash(i)] = i
        return i

    def add_new_item(self, itemType, label, **attrs):
        i = itemType(self, label, **attrs)
        return self.add_item(i)

    def items(self):
        return [(
         k, v) for k, v in list(module_globals.items()) if isinstance(v, BaseItem)]

    def values(self):
        for v in list(self.collection.values()):
            (yield v)

    def set_ids(self):
        for k, v in list(self.items()):
            v.id = k

    def get_first_item(self):
        return list(self.collection.values())[0]