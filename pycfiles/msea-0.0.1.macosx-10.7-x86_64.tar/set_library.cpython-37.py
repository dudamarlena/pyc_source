# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zichen/Documents/Yan/MSEA_python_package/venv37/lib/python3.7/site-packages/msea/set_library.py
# Compiled at: 2020-03-28 13:16:00
# Size of source mod 2**32: 4896 bytes
"""Handling microbe-set data structure and logistics.
"""
from __future__ import print_function
import os, warnings
from collections import Counter
import numpy as np
from .utils import *

class SetLibrary(object):
    __doc__ = 'SetLibrary is convenient class for a reference microbe-set library.\n    '

    def __init__(self, d_gmt=None, rank_means=None, rank_stds=None):
        """
        Construct a new 'SetLibrary' object.

        :param d_gmt: a dictionary representing the microbe-set library
        :param rank_means: (optional) the array of mean ranks from null distribution
        :param rank_stds: (optional) the array of standard deviations of ranks from null distribution
        :return: returns nothing
        """
        self.d_gmt = d_gmt
        self.rank_means = rank_means
        self.rank_stds = rank_stds
        if self.d_gmt:
            self._gather_all_items()

    def _gather_all_items(self):
        all_items = Counter()
        for item_set in self.d_gmt.values():
            all_items.update(item_set)

        self.all_items = all_items

    def get_empirical_ranks(self, n=1000, universe=1200, fix_size=None):
        """
        Calculate the empirical rank for each reference sets.

        :param n: number of permutations
        :param universe: number of microbes used as the universe size for Fisher's exact test
        :param fix_size: if None, uses variable sizes when generating random sets; if int,
            uses fixed size random sets to evaluate the null distribution of the ranks
        :return: returns nothing
        """
        print('Calculating empirical ranks for each set...')
        rank_means, rank_stds = get_empirical_ranks((self.d_gmt),
          n=n, universe=universe, fix_size=fix_size)
        self.rank_means = rank_means
        self.rank_stds = rank_stds

    def enrich(self, input_set, adjust=False, universe=1000):
        """
        Perform MSEA given an input_set.

        :param input_set: a set of microbes as the input for MSEA analysis against this reference set
        :param adjust: if True, adjust for the expected distributions of ranks
        :param universe: number of microbes used as the universe size for Fisher's exact test
        :return: returns a pandas.DataFrame object for the MSEA result table
        """
        unmapped_items = input_set - set(self.all_items.keys())
        if len(unmapped_items) == len(input_set):
            raise ValueError('There is no overlap between of the microbes in reference set and the input set.')
        else:
            if len(unmapped_items) > 0:
                warnings.warn('{} of the {} microbes in the input_set do(es) not exist in the reference set library: {}'.format(len(unmapped_items), len(input_set), ';'.join(list(unmapped_items))), RuntimeWarning)
            elif not adjust:
                result = enrich(input_set, (self.d_gmt), universe=universe)
            else:
                result = enrich(input_set,
                  (self.d_gmt),
                  rank_means=(self.rank_means), rank_stds=(self.rank_stds),
                  universe=universe)
            return result

    @classmethod
    def load(cls, gmt_file=None, rank_means_file=None, rank_stds_file=None):
        """
        Load a reference set into a SetLibrary instance from files.

        :param gmt_file: a file or url of a file for the reference set in GMT format
        :param rank_means_file: a .npy file for the array of mean ranks
        :param rank_stds_file: a .npy file for the array of std ranks
        :return: returns a SetLibrary object
        """
        d_gmt = read_gmt(gmt_file)
        rank_means = None
        rank_stds = None
        if rank_means_file:
            rank_means = np.load(rank_means_file)
        if rank_stds_file:
            rank_stds = np.load(rank_stds_file)
        return cls(d_gmt, rank_means, rank_stds)

    def save(self, dirname):
        """
        Save the SetLibrary instance in a directory,
        optionally with computed rank_means and rank_stds.

        :param dirname: directory name to which the object is going to be stored
        :return: returns nothing
        """
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        write_gmt(self.d_gmt, os.path.join(dirname, 'set_library.gmt'))
        if self.rank_means:
            np.save(os.path.join(dirname, 'rank_means.npy'), self.rank_means)
        if self.rank_stds:
            np.save(os.path.join(dirname, 'rank_stds.npy'), self.rank_stds)
        print('Set-library saved to {}'.format(dirname))