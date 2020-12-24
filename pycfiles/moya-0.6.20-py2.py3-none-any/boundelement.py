# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/elements/boundelement.py
# Compiled at: 2015-09-01 07:17:44
from __future__ import unicode_literals

class BoundElement(object):
    __slots__ = ('app', 'element')

    def __init__(self, app, element):
        self.app = app
        self.element = element

    @classmethod
    def from_tuple(cls, app_element):
        app, element = app_element
        return cls(app, element)

    def __repr__(self):
        return (b'<{1} in app {0}>').format(self.app, self.element)

    def __iter__(self):
        return iter(('app', 'element'))

    def __getitem__(self, key):
        if key == b'app':
            return self.app
        if key == b'element':
            return self.element
        raise KeyError(key)

    def __moyamodel__(self):
        return (
         self.app, self.element)

    def keys(self):
        return ('app', 'element')

    def iterkeys(self):
        return iter(self.keys())

    def values(self):
        return (
         self.app, self.element)

    def itervalues(self):
        return iter(self.values())

    def items(self):
        return [
         (
          b'app', self.app), (b'element', self.element)]

    def iteritems(self):
        return self.items()