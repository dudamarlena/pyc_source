# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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