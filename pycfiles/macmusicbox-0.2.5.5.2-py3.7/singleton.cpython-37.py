# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/NEMbox/singleton.py
# Compiled at: 2020-03-06 09:10:15
# Size of source mod 2**32: 579 bytes


class Singleton(object):
    __doc__ = "Singleton Class\n    This is a class to make some class being a Singleton class.\n    Such as database class or config class.\n\n    usage:\n        class xxx(Singleton):\n            def __init__(self):\n                if hasattr(self, '_init'):\n                    return\n                self._init = True\n                other init method\n    "

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = (super().__new__)(cls, *args, **kwargs)
        return cls._instance