# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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