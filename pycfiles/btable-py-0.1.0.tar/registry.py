# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bta/tools/registry.py
# Compiled at: 2014-07-11 17:28:38
from collections import defaultdict

class Registry(object):
    registry = defaultdict(dict)

    @classmethod
    def register(cls, **kargs):

        def do_reg(f, cls=cls, kargs=kargs):
            cls.registry[cls.__name__][f.__name__] = kargs
            return f

        return do_reg

    @classmethod
    def register_ref(cls, obj, key='__name__'):
        cls.registry[cls.__name__][getattr(obj, key)] = obj
        return obj

    @classmethod
    def get_all(cls):
        return cls.registry[cls.__name__]

    @classmethod
    def get(cls, name, default=None):
        return cls.registry[cls.__name__].get(name, default)

    @classmethod
    def iterkeys(cls):
        return iter(cls.registry[cls.__name__])

    @classmethod
    def iteritems(cls):
        return cls.registry[cls.__name__].iteritems()

    @classmethod
    def itervalues(cls):
        return cls.registry[cls.__name__].itervalues()