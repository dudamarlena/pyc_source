# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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