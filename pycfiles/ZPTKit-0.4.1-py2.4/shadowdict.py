# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ZPTKit/shadowdict.py
# Compiled at: 2006-06-20 16:13:48
try:
    from UserDict import DictMixin
except ImportError:
    from backports.UserDict import DictMixin

class ShadowDict(DictMixin):
    __module__ = __name__

    def __init__(self, component, attr):
        self.__dict__['_ShadowDict__component'] = component
        self.__dict__['_ShadowDict__attr'] = attr

    def __dict(self):
        return getattr(self.__component, self.__attr)

    def __getitem__(self, key):
        return self.__dict()[key]

    def __setitem__(self, key, value):
        self.__dict()[key] = value

    def __delitem__(self, key):
        del self.__dict()[key]

    def keys(self):
        return self.__dict().keys()

    def __contains__(self, key):
        return key in self.__dict()

    def __iter__(self):
        return iter(self.__dict())

    def iteritems(self):
        return self.__dict().iteritems()

    def __getattr__(self, key):
        if key.startswith('_'):
            raise AttributeError
        return self[key]

    def __setattr__(self, key, value):
        if key.startswith('_'):
            raise AttributeError
        self[key] = value