# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pytextgrid/PraatTierIterator.py
# Compiled at: 2018-12-13 05:11:22
# Size of source mod 2**32: 4049 bytes
import exceptions
from PraatTextGrid import Interval

class PraatTierIterator:

    def __init__(self):
        raise NotImplementedError

    def __iter__(self):
        return self


class ExcludeListTierIterator:
    __doc__ = '\n    iterate on a given praat tier and exclude intervals\n    whose text is contained in a list/set given at instance creation\n    '

    def __init__(self, tier, exclude_set=[]):
        self._it = tier.__iter__()
        self._exclude_set = set(exclude_set)

    def next(self):
        res = self._it.next()
        while res._text in self._exclude_set:
            res = self._it.next()

        return res