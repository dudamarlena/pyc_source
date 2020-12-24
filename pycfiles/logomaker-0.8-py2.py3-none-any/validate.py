# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../../logomaker/src/validate.py
# Compiled at: 2019-04-23 15:38:05
from __future__ import division
import numpy as np, pandas as pd
from logomaker.src.error_handling import check, handle_errors

@handle_errors
def validate_matrix(df, matrix_type=None, allow_nan=False):
    """
    Checks to make sure that the input dataframe, df, represents a valid
    matrix, i.e., an object that can be displayed as a logo.

    parameters
    ----------

    df: (dataframe)
        A pandas dataframe where each row represents an (integer) position
        and each column represents to a (single) character.

    matrix_type: (None or str)
        If 'probability', validates df as a probability matrix, i.e., all
        elements are in [0,1] and rows are normalized). If 'information',
        validates df as an information matrix, i.e., all elements >= 0.

    allow_nan: (bool)
        Whether to allow NaN entries in the matrix.

    returns
    -------
    out_df: (dataframe)
        A cleaned-up version of df (if possible).
    """
    check(isinstance(df, pd.DataFrame), 'out_df needs to be a valid pandas out_df, out_df entered: %s' % type(df))
    out_df = df.copy()
    check(matrix_type in {None, 'probability', 'information'}, 'matrix_type = %s; must be None, "probability", or "information"' % matrix_type)
    check(isinstance(allow_nan, bool), 'allow_nan must be of type bool; is type %s.' % type(allow_nan))
    if not allow_nan:
        check(np.isfinite(out_df.values).all(), 'some matrix elements are not finite. Set allow_nan=True to allow this.')
    check(out_df.shape[0] >= 1, 'df has zero rows. Needs multiple rows.')
    check(out_df.shape[1] >= 1, 'df has zero columns. Needs multiple columns.')
    for i, col in enumerate(out_df.columns):
        col = str(col)
        check(isinstance(col, str), 'column number %d is of type %s; must be a str' % (i, col))
        check(len(col) == 1, 'column %d is %s and has length %d; ' % (i, repr(col), len(col)) + 'must have length 1.')

    char_cols = list(out_df.columns)
    char_cols.sort()
    out_df = out_df[char_cols]
    out_df.index.name = 'pos'
    try:
        int_index = out_df.index.astype(int)
    except TypeError:
        check(False, 'could not convert df.index to type int. Check that all positions have integer numerical values.')

    check(all(int_index == out_df.index), 'could not convert df.index values to int without changingsome values. Make sure that df.index values are integers.')
    check(len(set(out_df.index)) == len(out_df.index), 'not all values of df.index are unique. Make sure all are unique.')
    if matrix_type is 'information':
        check(all(df.values.ravel() >= 0), 'not all values in df are >=0.')
    elif matrix_type is 'probability':
        check(all(df.values.ravel() >= 0), 'not all values in df are >=0.')
        sums = df.sum(axis=1).values
        check(not any(np.isclose(sums, 0.0)), 'some columns in df sum to nearly zero.')
        if not all(np.isclose(sums, 1.0)):
            print 'in validate_matrix(): Row sums in df are not close to 1. Reormalizing rows...'
            df.loc[:, :] = df.values / sums[:, np.newaxis]
            out_df = df.copy()
    elif matrix_type is None:
        pass
    return out_df


@handle_errors
def validate_probability_mat(df):
    """
    Verifies that the input dataframe df indeed represents a
    probability matrix. Renormalizes df with a text warning if it is not
    already normalized. Throws an error if df cannot be reliably normalized.

    parameters
    ----------

    df: (dataframe)
        A pandas dataframe where each row represents an (integer) position
        and each column represents to a (single) character.

    returns
    -------
    prob_df: (dataframe)
        A cleaned-up and normalized version of df (if possible).
    """
    prob_df = validate_matrix(df, allow_nan=False)
    check(all(prob_df.values.ravel() >= 0), 'not all values in df are >=0.')
    sums = prob_df.sum(axis=1).values
    check(not any(np.isclose(sums, 0.0)), 'some columns in prob_df sum to nearly zero.')
    if not all(np.isclose(sums, 1.0)):
        print 'in validate_probability_mat(): Row sums in df are not close to 1. Reormalizing rows...'
        prob_df.loc[:, :] = prob_df.values / sums[:, np.newaxis]
    return prob_df