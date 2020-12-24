# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\tsp\filters\smoothing.py
# Compiled at: 2018-01-14 22:14:26
# Size of source mod 2**32: 1135 bytes
"""
Filters that apply smoothing operations on other filters.

These are generally useful for controlling/minimizing turnover on existing
Filters.
"""
from .filter import CustomFilter

class All(CustomFilter):
    __doc__ = '\n    A Filter requiring that assets produce True for ``window_length``\n    consecutive days.\n\n    **Default Inputs:** None\n\n    **Default Window Length:** None\n    '

    def compute(self, today, assets, out, arg):
        out[:] = arg.sum(axis=0) == self.window_length


class Any(CustomFilter):
    __doc__ = '\n    A Filter requiring that assets produce True for at least one day in the\n    last ``window_length`` days.\n\n    **Default Inputs:** None\n\n    **Default Window Length:** None\n    '

    def compute(self, today, assets, out, arg):
        out[:] = arg.sum(axis=0) > 0


class AtLeastN(CustomFilter):
    __doc__ = '\n    A Filter requiring that assets produce True for at least N days in the\n    last ``window_length`` days.\n\n    **Default Inputs:** None\n\n    **Default Window Length:** None\n    '
    params = ('N', )

    def compute(self, today, assets, out, arg, N):
        out[:] = arg.sum(axis=0) >= N