# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/zensols/multi/reducer.py
# Compiled at: 2020-05-02 23:35:41
# Size of source mod 2**32: 1572 bytes
"""Stash extensions to distribute item creation over multiple processes.

"""
__author__ = 'Paul Landes'
import logging, math
from multiprocessing import Pool
from zensols.persist import Stash
logger = logging.getLogger(__name__)

class StashMapReducer(object):
    __doc__ = 'Process work in sub processes from data in a stash.\n\n    '

    def __init__(self, stash: Stash, n_workers: int=10):
        self.stash = stash
        self.n_workers = n_workers

    @property
    def key_group_size(self):
        n_items = len(self.stash)
        return math.ceil(n_items / self.n_workers)

    def _map(self, id: str, val):
        return (id, val)

    def _reduce(self, vals):
        return vals

    def _reduce_final(self, reduced_vals):
        return reduced_vals

    def _map_ids(self, id_sets):
        return tuple(map(lambda id: self._map(id, self.stash[id]), id_sets))

    def map(self):
        id_sets = self.stash.key_groups(self.key_group_size)
        pool = Pool(self.n_workers)
        return pool.map(self._map_ids, id_sets)

    def __call__(self):
        mapval = self.map()
        reduced = map(self._reduce, mapval)
        return self._reduce_final(reduced)


class FunctionStashMapReducer(StashMapReducer):

    def __init__(self, stash, func, n_workers=10):
        super().__init__(stash, n_workers)
        self.func = func

    def _map(self, id: str, val):
        return self.func(id, val)

    @staticmethod
    def map_func(*args, **kwargs):
        mr = FunctionStashMapReducer(*args, **kwargs)
        return mr.map()