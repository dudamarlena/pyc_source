# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/pytq-project/pytq/pkg/attrs_mate/mate.py
# Compiled at: 2017-11-23 13:02:06
import attr, collections

class AttrsClass(object):

    def keys(self):
        return [ a.name for a in self.__attrs_attrs__ ]

    def values(self):
        return [ getattr(self, a.name) for a in self.__attrs_attrs__ ]

    def items(self):
        return list(zip(self.keys(), self.values()))

    def to_dict(self):
        return attr.asdict(self)

    def to_OrderedDict(self):
        return collections.OrderedDict(self.items())