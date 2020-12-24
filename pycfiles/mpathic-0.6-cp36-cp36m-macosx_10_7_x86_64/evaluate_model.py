# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: mpathic/src/evaluate_model.py
# Compiled at: 2018-06-21 15:21:36
"""A script which adds a predicted energy column to an input table. This is
    generated based on a energy model the user provides."""
from __future__ import division
from mpathic.src import Models
from mpathic.src import utils
from mpathic.src import qc
from mpathic.src import io_local as io
from mpathic import SortSeqError
from mpathic import shutthefuckup
from mpathic.src import fast

class EvaluateModel:
    """

    Parameters
    ----------

    dataset_df: (pandas dataframe)
        Input dataset data frame
    model_df: (pandas dataframe)
        Model dataframe
    left: (int)
        Seq position at which to align the left-side of the model. 

        Defaults to position determined by model dataframe.

    right: (int)
        Seq position at which to align the right-side of the model. 

        Defaults to position determined by model dataframe.

    """

    def __init__(self, dataset_df, model_df, left=None, right=None):
        self.dataset_with_values = None
        self.out_df = None
        qc.validate_dataset(dataset_df)
        qc.validate_model(model_df)
        seqtype, modeltype = qc.get_model_type(model_df)
        seqcol = qc.seqtype_to_seqcolname_dict[seqtype]
        if not (left is None or right is None):
            raise SortSeqError('Cannot set both left and right at same time.')
        if left is not None:
            start = left
            end = start + model_df.shape[0] + (1 if modeltype == 'NBR' else 0)
        elif right is not None:
            end = right
            start = end - model_df.shape[0] - (1 if modeltype == 'NBR' else 0)
        else:
            start = model_df['pos'].values[0]
            end = model_df['pos'].values[(-1)] + (2 if modeltype == 'NBR' else 1)
        assert start < end
        seq_length = len(dataset_df[seqcol][0])
        if start < 0:
            raise SortSeqError('Invalid start=%d' % start)
        if end > seq_length:
            raise SortSeqError('Invalid end=%d for seq_length=%d' % (end, seq_length))
        out_df = dataset_df.copy()
        out_df.loc[:, seqcol] = out_df.loc[:, seqcol].str.slice(start, end)
        if modeltype == 'MAT':
            mymodel = Models.LinearModel(model_df)
        elif modeltype == 'NBR':
            mymodel = Models.NeighborModel(model_df)
        else:
            raise SortSeqError('Unrecognized model type %s' % modeltype)
        out_df['val'] = mymodel.evaluate(out_df)
        self.dataset_with_values = qc.validate_dataset(out_df, fix=True)
        self.out_df = out_df
        return