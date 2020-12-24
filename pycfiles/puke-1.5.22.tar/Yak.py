# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: puke/Yak.py
# Compiled at: 2011-12-05 13:53:38


class Yak(dict):

    class __metaclass__(type):

        def __iter__(self):
            for attr in dir(Yak):
                if not attr.startswith('__'):
                    yield attr

    @staticmethod
    def set(key, value):
        setattr(Yak, key, value)

    @staticmethod
    def get(key, default=None):
        try:
            return getattr(Yak, key)
        except:
            return default