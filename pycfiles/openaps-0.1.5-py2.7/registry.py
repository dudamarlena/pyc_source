# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/openaps/uses/registry.py
# Compiled at: 2015-12-15 13:09:24


class Registry(object):

    def __init__(self):
        self.__USES__ = {}

    def get_uses(self, device, config):
        all_uses = self.__USES__.values()
        all_uses.sort(key=lambda usage: getattr(usage, 'sortOrder', usage.__name__))
        return all_uses

    def __call__(self):

        def decorator(cls):
            if cls.__name__ not in self.__USES__:
                self.__USES__[cls.__name__] = cls
            return cls

        return decorator