# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../../logomaker/src/data.py
# Compiled at: 2019-03-13 14:05:30
# Size of source mod 2**32: 16865 bytes
from __future__ import division
import numpy as np, pandas as pd, pdb
from logomaker.src.validate import validate_matrix, validate_probability_mat, validate_information_mat
iupac_dict = {'A':'A', 
 'C':'C', 
 'G':'G', 
 'T':'T', 
 'R':'AG', 
 'Y':'CT', 
 'S':'GC', 
 'W':'AT', 
 'K':'GT', 
 'M':'AC', 
 'B':'CGT', 
 'D':'AGT', 
 'H':'ACT', 
 'V':'ACG', 
 'N':'ACGT'}
SMALL = np.finfo(float).tiny

def transform_matrix(df, from_type, to_type, background=None, pseudocount=1, center=False):
    """
    Transforms a matrix of one type into a matrix of another type.

    i = position
    c, d = character

    l = pseudocount
    C = number of characters

    N_ic = counts matrix element
    P_ic = probability matrix element
    Q_ic = background probability matrix element
    W_ic = weight matrix element
    I_ic = information matrix element

    counts -> probability:
        P_ic = (N_ic + l)/(N_i + C*l), N_i = sum_c(N_ic)

    probability -> weight:
        W_ic = log_2(P_ic / Q_ic)

    weight -> probability:
        P_ic = Q_ic * 2^(W_ic)

    probability -> information:
        I_ic = P_ic * sum_d(P_id * log2(P_id / W_id))

    information -> probability:
        P_ic = I_ic / sum_d(I_id)

    parameters
    ----------

    df: (dataframe)
        The matrix to be transformed.

    from_type: (str)
        Type of input matrix. Must be one of 'counts', 'probability',
        'weight', or 'information'.

    to_type: (str)
        Type of output matrix. Must be one of 'probability', 'weight', or
        'information'. Can NOT be 'counts'.

    background: (array, or df)
        Specification of background probabilities. If array, should be the
        same length as df.columns and correspond to the probability of each
        column's character. If df, should be a probability matrix the same
        shape as df.

    pseudocount: (number >= 0)
        Pseudocount to use when transforming from a count matrix to a
        probability matrix.

    center: (bool)
        Whether to center the output matrix. Note: this only works when
        to_type = 'weight', as centering a matrix doesn't make sense otherwise.

    returns
    -------
    out_df: (dataframe)
        Transformed matrix
    """
    FROM_TYPES = {
     'counts', 'probability', 'weight', 'information'}
    TO_TYPES = {'probability', 'weight', 'information'}
    df = validate_matrix(df)
    if from_type == to_type:
        out_df = df.copy()
    else:
        assert from_type in FROM_TYPES, 'Error: invalid from_type=%s' % from_type
        if not to_type in TO_TYPES:
            raise AssertionError('Error: invalid to_type="%s"' % from_type)
    if from_type == 'probability':
        if to_type == 'weight':
            out_df = _probability_mat_to_weight_mat(df, background)
        elif to_type == 'information':
            out_df = _probability_mat_to_information_mat(df, background)
    else:
        if from_type == 'counts':
            prob_df = _counts_mat_to_probability_mat(df, pseudocount)
        else:
            if from_type == 'weight':
                prob_df = _weight_mat_to_probability_mat(df, background)
            else:
                if from_type == 'information':
                    prob_df = _information_mat_to_probability_mat(df, background)
                else:
                    assert False, 'THIS SHOULD NEVER HAPPEN'
                    out_df = transform_matrix(prob_df, from_type='probability',
                      to_type=to_type,
                      background=background)
    if center:
        assert to_type == 'weight', 'Error: the option center=True is only compatible with ' + 'to_type == "weight"'
        out_df = center_matrix(out_df)
    out_df = validate_matrix(out_df)
    return out_df


def _counts_mat_to_probability_mat(df, pseudocount=1.0):
    """
    Converts a counts matrix to a probability matrix
    """
    assert pseudocount >= 0, 'Error: Pseudocount must be >= 0. '
    df = validate_matrix(df)
    out_df = df.copy()
    vals = df.values + pseudocount
    out_df.loc[:, :] = vals / vals.sum(axis=1)[:, np.newaxis]
    out_df = normalize_matrix(out_df)
    out_df = validate_probability_mat(out_df)
    return out_df


def _probability_mat_to_weight_mat(df, background=None):
    """
    Converts a probability matrix to a weight matrix
    """
    df = validate_probability_mat(df)
    bg_df = _get_background_mat(df, background)
    out_df = df.copy()
    out_df.loc[:, :] = np.log2(df + SMALL) - np.log2(bg_df + SMALL)
    out_df = validate_matrix(out_df)
    return out_df


def _weight_mat_to_probability_mat(df, background=None):
    """
    Converts a probability matrix to a weight matrix
    """
    df = validate_matrix(df)
    bg_df = _get_background_mat(df, background)
    out_df = df.copy()
    out_df.loc[:, :] = bg_df.values * np.power(2, df.values)
    out_df = normalize_matrix(out_df)
    out_df = validate_probability_mat(out_df)
    return out_df


def _probability_mat_to_information_mat(df, background=None):
    """
    Converts a probability matrix to an information matrix
    """
    df = validate_probability_mat(df)
    bg_df = _get_background_mat(df, background)
    out_df = df.copy()
    fg_vals = df.values
    bg_vals = bg_df.values
    tmp_vals = fg_vals * (np.log2(fg_vals + SMALL) - np.log2(bg_vals + SMALL))
    info_vec = tmp_vals.sum(axis=1)
    out_df.loc[:, :] = fg_vals * info_vec[:, np.newaxis]
    out_df = validate_information_mat(out_df)
    return out_df


def _information_mat_to_probability_mat(df, background=None):
    """
    Converts a probability matrix to an information matrix
    """
    df = validate_matrix(df)
    out_df = normalize_matrix(df)
    out_df = validate_probability_mat(out_df)
    return out_df


def normalize_matrix(df):
    """
    Normalizes a matrix df to a probability matrix out_df
    """
    df = validate_matrix(df)
    if not all(df.values.ravel() >= 0):
        raise AssertionError('Error: Some data frame entries are negative.')
    else:
        sums = df.sum(axis=1).values
        assert not any(np.isclose(sums, 0.0)), 'Error: some columns in df sum to nearly zero.'
    out_df = df.copy()
    out_df.loc[:, :] = df.values / sums[:, np.newaxis]
    out_df = validate_probability_mat(out_df)
    return out_df


def center_matrix(df):
    """
    Centers each row of a matrix about zero by subtracting out the mean.
    """
    df = validate_matrix(df)
    means = df.mean(axis=1).values
    out_df = df.copy()
    out_df.loc[:, :] = df.values - means[:, np.newaxis]
    out_df = validate_matrix(out_df)
    return out_df


def _get_background_mat(df, background):
    """
    Creates a background matrix given a background specification. There
    are three possiblities:

    1. background is None => out_df represents a uniform background
    2. background is a vector => this vector is normalized then used as
        the entries of the rows of out_df
    3. background is a dataframe => it is then normalized and use as out_df
    """
    num_pos, num_cols = df.shape
    out_df = df.copy()
    if background is None:
        out_df.loc[:, :] = 1 / num_cols
    else:
        if isinstance(background, (np.ndarray, list, tuple)):
            background = np.array(background)
            assert len(background) == num_cols, 'Error: df and background have mismatched dimensions.'
            out_df.loc[:, :] = background[np.newaxis, :]
            out_df = normalize_matrix(out_df)
        else:
            if isinstance(background, pd.core.frame.DataFrame):
                background = validate_matrix(background)
                assert all(df.index == background.index), 'Error: df and bg_mat have different indexes.'
                assert all(df.columns == background.columns), 'Error: df and bg_mat have different columns.'
                out_df = background.copy()
                out_df = normalize_matrix(out_df)
    out_df = validate_probability_mat(out_df)
    return out_df


def iupac_to_matrix(iupac_seq, to_type='probability', **kwargs):
    """
    Generates a matrix corresponding to a (DNA) IUPAC string.

    parameters
    ----------
    iupac_seq: (str)
        An IUPAC sequence.

    to_type: (str)
        The type of matrix to convert to. Must be 'probability', 'weight',
        or 'information'

    **kwargs:
        Additional arguments to send to transform_matrix, e.g. background
        or center

    returns
    -------
    out_df: (dataframe)
        A matrix of the requested type.
    """
    L = len(iupac_seq)
    cols = list('ACGT')
    index = list(range(L))
    counts_mat = pd.DataFrame(data=0.0, columns=cols, index=index)
    for i, c in enumerate(list(iupac_seq)):
        bs = iupac_dict[c]
        for b in bs:
            counts_mat.loc[(i, b)] = 1

    out_df = transform_matrix(counts_mat, pseudocount=0,
      from_type='counts',
      to_type=to_type)
    return out_df


def alignment_to_matrix(sequences, to_type='counts', characters_to_ignore='.-', **kwargs):
    """
    Generates matrix from a sequence alignment

    parameters
    ----------
    sequences: (list of str)
        An list of sequences, all of which must be the same length

    to_type: (str)
        The type of matrix to output. Must be 'counts', 'probability',
        'weight', or 'information'

    **kwargs:
        Other arguments to pass to logomaker.transform_matrix(), e.g.
        pseudocount

    returns
    -------
    out_df: (dataframe)
        A matrix of the requested type.
    """
    char_array = np.array([np.array(list(seq)) for seq in sequences])
    L = char_array.shape[1]
    unique_characters = np.unique(char_array.ravel())
    unique_characters.sort()
    columns = [c for c in unique_characters if c not in characters_to_ignore]
    index = list(range(L))
    counts_df = pd.DataFrame(data=0, columns=columns, index=index)
    for c in columns:
        counts_df.loc[:, c] = (char_array == c).astype(float).sum(axis=0).ravel()

    out_df = transform_matrix(counts_df, from_type='counts', 
     to_type=to_type, **kwargs)
    return out_df