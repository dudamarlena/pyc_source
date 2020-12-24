# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: mpathic/src/profile_freq.py
# Compiled at: 2018-06-21 15:23:40
"""
Calculates the fractional number of character occurances at each position within the set of sequences passed.
"""
from __future__ import division
import argparse, numpy as np, sys, pandas as pd
from mpathic.src import qc
from mpathic.src import io_local as io
from mpathic.src import profile_ct
import pdb
from mpathic import SortSeqError
from mpathic.src.utils import handle_errors, check, ControlledError

class ProfileFreq:
    """

    Profile Frequencies computes character frequencies (0.0 to 1.0) at each position

    Parameters
    ----------
    dataset_df: (pandas dataframe)
        A dataframe containing a valid dataset.

    bin: (int)
        A bin number specifying which counts to use

    start: (int)
        An integer specifying the sequence start position

    end: (int)
        An integer specifying the sequence end position

    Returns
    -------
    freq_df: (pd.DataFrame)
        A dataframe containing counts for each nucleotide/amino 

        acid character at each position.

    """

    @handle_errors
    def __init__(self, dataset_df=None, bin=None, start=0, end=None):
        self.dataset_df = dataset_df
        self.bin = bin
        self.start = start
        self.end = end
        self.freq_df = None
        self._input_check()
        counts_df = profile_ct.main(dataset_df, bin=bin, start=start, end=end)
        ct_cols = [ c for c in counts_df.columns if qc.is_col_type(c, 'ct_') ]
        freq_cols = [ 'freq_' + c.split('_')[1] for c in ct_cols ]
        freq_df = counts_df[ct_cols].div(counts_df['ct'], axis=0)
        freq_df.columns = freq_cols
        freq_df['pos'] = counts_df['pos']
        freq_df = qc.validate_profile_freq(freq_df, fix=True)
        self.freq_df = freq_df
        return

    def _input_check(self):
        """
        check input parameters for correctness
        """
        if self.dataset_df is None:
            raise ControlledError(" Profile freq requires pandas dataframe as input dataframe. Entered df was 'None'.")
        elif self.dataset_df is not None:
            check(isinstance(self.dataset_df, pd.DataFrame), 'type(df) = %s; must be a pandas dataframe ' % type(self.dataset_df))
            check(pd.DataFrame.equals(self.dataset_df, qc.validate_dataset(self.dataset_df)), ' Input dataframe failed quality control,                   please ensure input dataset has the correct format of an mpathic dataframe ')
        if self.bin is not None:
            check(isinstance(self.bin, int), 'type(bin) = %s; must be of type int ' % type(self.bin))
            check(self.bin > 0, 'bin = %d must be a positive int ' % self.bin)
        check(isinstance(self.start, int), 'type(start) = %s; must be of type int ' % type(self.start))
        check(self.start >= 0, 'start = %d must be a positive integer ' % self.start)
        if self.end is not None:
            check(isinstance(self.end, int), 'type(end) = %s; must be of type int ' % type(self.end))
        return