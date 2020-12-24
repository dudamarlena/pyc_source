# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/onema/Code/python/evee/build/lib/evee/event.py
# Compiled at: 2016-02-09 01:21:42
# Size of source mod 2**32: 245 bytes


class Event(object):

    def __init__(self):
        self._Event__propagation_stopped = False

    def is_propagation_stopped(self):
        return self._Event__propagation_stopped

    def stop_propagation(self):
        self._Event__propagation_stopped = True