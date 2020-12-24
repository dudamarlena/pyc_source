# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tareen/Desktop/MPAthic/PyPI_Staging_MPAthic_py_2_3/MPAthic/mpathic/src/profile_mut.py
# Compiled at: 2018-07-12 07:39:54
# Size of source mod 2**32: 4527 bytes
"""
This class calculates the fractional number of character occurances at each position within the set of sequences
passed. Specificially, it computes the mutation rate (0.0 to 1.0) at each position. Mutation rate is defined as
1.0 minus the maximum character frequency at a position. Errors are estimated using bionomial uncertainty

"""
from __future__ import division
import numpy as np, sys, pandas as pd
from mpathic.src import qc
from mpathic.src import io_local as io
from mpathic.src import profile_ct
import pdb
from mpathic import SortSeqError
from mpathic.src.utils import ControlledError, handle_errors, check

class ProfileMut:
    __doc__ = '\n\n    Parameters\n    ----------\n\n    dataset_df: (pandas dataframe)\n        Input data frame containing a valid dataset.\n\n    bin: (int)\n        A bin number specifying which counts to use\n\n    start: (int)\n        An integer specifying the sequence start position\n\n    end: (int)\n        An integer specifying the sequence end position\n\n    err: (boolean)\n        If true, include error estimates in computed mutual information\n\n    Returns\n    -------\n    mut_df: (pandas data frame)\n            A pandas dataframe containing results.\n    '

    @handle_errors
    def __init__(self, dataset_df=None, bin=None, start=0, end=None, err=False):
        self.dataset_df = dataset_df
        self.bin = bin
        self.start = start
        self.end = end
        self.err = err
        self.mut_df = None
        self._input_checks()
        counts_df = profile_ct.main(dataset_df, bin=bin, start=start, end=end)
        ct_cols = [c for c in counts_df.columns if qc.is_col_type(c, 'ct_')]
        mut_df = counts_df[['pos']].copy()
        max_ct = counts_df[ct_cols].max(axis=1)
        sum_ct = counts_df[ct_cols].sum(axis=1)
        mut = 1.0 - max_ct / sum_ct
        mut_df['mut'] = mut
        if err:
            mut_err = np.sqrt(mut * (1.0 - mut) / sum_ct)
            mut_df['mut_err'] = mut_err
        alphabet = ''.join([c.split('_')[1] for c in ct_cols])
        seqtype = qc.alphabet_to_seqtype_dict[alphabet]
        wt_col = qc.seqtype_to_wtcolname_dict[seqtype]
        mut_df[wt_col] = 'X'
        for col in ct_cols:
            indices = (counts_df[col] == max_ct).values
            mut_df.loc[(indices, wt_col)] = col.split('_')[1]

        mut_df = qc.validate_profile_mut(mut_df, fix=True)
        self.mut_df = mut_df

    def _input_checks(self):
        if self.dataset_df is None:
            raise ControlledError(" Profile info requires pandas dataframe as input dataframe. Entered df was 'None'.")
        else:
            if self.dataset_df is not None:
                check(isinstance(self.dataset_df, pd.DataFrame), 'type(df) = %s; must be a pandas dataframe ' % type(self.dataset_df))
                check(pd.DataFrame.equals(self.dataset_df, qc.validate_dataset(self.dataset_df)), ' Input dataframe failed quality control,                   please ensure input dataset has the correct format of an mpathic dataframe ')
            if self.bin is not None:
                check(isinstance(self.bin, int), 'type(bin) = %s; must be a int ' % type(self.bin))
            check(isinstance(self.start, int), 'type(start) = %s; must be of type int ' % type(self.start))
            check(self.start >= 0, 'start = %d must be a positive integer ' % self.start)
            if self.end is not None:
                check(isinstance(self.end, int), 'type(end) = %s; must be of type int ' % type(self.end))
        check(isinstance(self.err, bool), 'type(err) = %s; must be a boolean ' % type(self.err))