# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: c:\users\billingtonm\dropbox\code\pydiagrams\build\lib\pydiagrams\baseItems.py
# Compiled at: 2019-10-20 22:32:24
# Size of source mod 2**32: 1710 bytes
import sys
from collections import OrderedDict
module_globals = sys.modules['__main__'].__dict__

class BaseItem(object):
    """BaseItem"""

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
    """BaseItemCollection"""

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
            yield v

    def set_ids(self):
        for k, v in list(self.items()):
            v.id = k

    def get_first_item(self):
        return list(self.collection.values())[0]