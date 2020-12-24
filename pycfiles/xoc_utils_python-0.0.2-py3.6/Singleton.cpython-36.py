# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/xoc_utils/Singleton.py
# Compiled at: 2018-05-16 15:58:08
# Size of source mod 2**32: 441 bytes


class Singleton(type):
    __doc__ = '\n    Define an Instance operation that lets clients access its unique\n    instance.\n    '

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = (super().__call__)(*args, **kwargs)
        return cls._instance