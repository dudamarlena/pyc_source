# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /src/colin/utils/caching_iterable.py
# Compiled at: 2018-05-10 03:52:50
# Size of source mod 2**32: 492 bytes
import itertools

class CachingIterable(object):

    def __init__(self, iterable):
        self.iterable = iterable
        self.iter = iter(iterable)
        self.done = False
        self.vals = []

    def __iter__(self):
        if self.done:
            return iter(self.vals)
        else:
            return itertools.chain(self.vals, self._gen_iter())

    def _gen_iter(self):
        for new_val in self.iter:
            self.vals.append(new_val)
            yield new_val

        self.done = True