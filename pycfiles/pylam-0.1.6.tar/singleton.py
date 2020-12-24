# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.6/site-packages/PyLAF/utils/core/singleton.py
# Compiled at: 2011-02-04 03:54:22


class Singleton(type):

    def __init__(self, *args):
        type.__init__(self, *args)
        self._instances = {}

    def __call__(self, *args):
        if args not in self._instances:
            self._instances[args] = type.__call__(self, *args)
        return self._instances[args]