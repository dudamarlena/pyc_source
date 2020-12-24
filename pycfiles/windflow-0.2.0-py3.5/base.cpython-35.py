# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/windflow/services/base.py
# Compiled at: 2018-04-18 11:33:58
# Size of source mod 2**32: 342 bytes


class Service:
    __doc__ = '\n    Service singleton implementation.\n\n    '

    @classmethod
    def factory(cls, **kwargs):
        return super().__new__(cls)

    def __new__(cls, **kw):
        try:
            return cls._instance
        except AttributeError as e:
            cls._instance = cls.factory(**kw)

        return cls._instance