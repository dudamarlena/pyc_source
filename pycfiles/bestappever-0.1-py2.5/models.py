# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/bestappever/models.py
# Compiled at: 2008-08-25 06:10:07
from zope.interface import Interface
from zope.interface import implements
from zope.location.interfaces import ILocation

class IMyModel(Interface):
    pass


class MyModel(object):
    implements(IMyModel, ILocation)
    __name__ = None
    __parent__ = None

    def __getitem__(self, name):
        return MyModel()

    def absolute_path(self):
        p = []
        node = self
        while node.__name__ is not None:
            p.append(node.__name__)
            node = node.__parent__

        p.reverse()
        return ('/').join(p)


root = MyModel()

def get_root(environ):
    return root