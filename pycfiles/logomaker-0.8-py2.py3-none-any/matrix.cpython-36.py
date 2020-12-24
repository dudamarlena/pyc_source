# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../../logomaker/src/matrix.py
# Compiled at: 2019-05-09 11:28:34
# Size of source mod 2**32: 27960 bytes
from __future__ import division
import numpy as np, pandas as pd
from logomaker.src.error_handling import check, handle_errors
from logomaker.src.validate import validate_matrix
ALPHABET_DICT = {'dna':'ACGT', 
 'rna':'ACGU', 
 'protein':'ACDEFGHIKLMNPQRSTVWY'}
IUPAC_DICT = {'A':'A', 
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
MATRIX_TYPES = {'counts', 'probability', 'weight', 'information'}

@handle_errors
def transform_matrix(df, center_values=False, normalize_values=False, from_type=None, to_type=None, background=None, pseudocount=1):
    """
    Performs transformations on a matrix. There are three types of
    transformations that can be performed:

    1. Center values:
        Subtracts the mean from each row in df. This is common for weight
        matrices or energy matrices. To do this, set center_values=True.

    2. Normalize values:
        Divides each row by the sum of the row. This is needed for probability
        matrices. To do this, set normalize_values=True.

    3. From/To transformations:
        Transforms from one type of matrix (e.g. 'counts') to another type
        of matrix (e.g. 'information'). To do this, set from_type and to_type
        arguments.

    Here are the mathematical formulas invoked by From/To transformations:

        from_type='counts' ->  to_type='probability':
            P_ic = (N_ic + l)/(N_i + C*l), N_i = sum_c(N_ic)

        from_type='probability' -> to_type='weight':
            W_ic = log_2(P_ic / Q_ic)

        from_type='weight' -> to_type='probability':
            P_ic = Q_ic * 2^(W_ic)

        from_type='probability' -> to_type='information':
            I_ic = P_ic * sum_d(P_id * log2(P_id / W_id))

        from_type='information' -> to_type='probability':
            P_ic = I_ic / sum_d(I_id)

        notation:
            i = position
            c, d = character
            l = pseudocount
            C = number of characters
            N_ic = counts matrix element
            P_ic = probability matrix element
            Q_ic = background probability matrix element
            W_ic = weight matrix element
            I_ic = information matrix element

    Using these five 1-step transformations, 2-step transformations
    are also enabled, e.g., from_type='counts' -> to_type='information'.

    parameters
    ----------

    df: (dataframe)
        The matrix to be transformed.

    center_values: (bool)
        Whether to center matrix values, i.e., subtract the mean from each
        row.

    normalize_values: (bool)
        Whether to normalize each row, i.e., divide each row by
        the sum of that row.

    from_type: (str)
        Type of input matrix. Must be one of 'counts', 'probability',
        'weight', or 'information'.

    to_type: (str)
        Type of output matrix. Must be one of 'probability', 'weight', or
        'information'. Can be 'counts' ONLY if from_type is 'counts' too.

    background: (array, or df)
        Specification of background probabilities. If array, should be the
        same length as df.columns and correspond to the probability of each
        column's character. If df, should be a probability matrix the same
        shape as df.

    pseudocount: (number >= 0)
        Pseudocount to use when transforming from a counts matrix to a
        probability matrix.

    returns
    -------
    out_df: (dataframe)
        Transformed matrix
    """
    df = validate_matrix(df)
    check(isinstance(center_values, bool), 'type(center_values) = %s must be of type bool' % type(center_values))
    check(isinstance(normalize_values, bool), 'type(normalize_values) = %s must be of type bool' % type(normalize_values))
    check(from_type in MATRIX_TYPES or from_type is None, 'from_type = %s must be None or in %s' % (
     from_type, MATRIX_TYPES))
    check(to_type in MATRIX_TYPES or to_type is None, 'to_type = %s must be None or in %s' % (
     to_type, MATRIX_TYPES))
    check(isinstance(background, (type([]), np.ndarray, pd.DataFrame)) or background is None, 'type(background) = %s must be None or array-like or a dataframe.' % type(background))
    check(isinstance(pseudocount, (int, float)), 'type(pseudocount) = %s must be a number' % type(pseudocount))
    check(pseudocount >= 0, 'pseudocount=%s must be >= 0' % pseudocount)
    if center_values is True:
        check(from_type is None and to_type is None, 'If center_values is True, both from_type and to_typemust be None. Here, from_type=%s, to_type=%s' % (
         from_type, to_type))
        out_df = _center_matrix(df)
    else:
        if normalize_values is True:
            check(from_type is None and to_type is None, 'If normalize_values is True, both from_type and to_typemust be None. Here, from_type=%s, to_type=%s' % (
             from_type, to_type))
            out_df = _normalize_matrix(df)
        else:
            if from_type == to_type:
                out_df = df.copy()
            else:
                check(from_type is not None and to_type is not None, 'Unless center_values is True or normalize_values is True,Neither from_type (=%s) nor to_type (=%s) can be None.' % (
                 from_type, to_type))
                check(to_type != 'counts', "Can only have to_type='counts' if from_type='counts'. Here, however, from_type='%s'" % from_type)
                if from_type == 'probability':
                    if to_type == 'weight':
                        out_df = _probability_mat_to_weight_mat(df, background)
                    else:
                        if to_type == 'information':
                            out_df = _probability_mat_to_information_mat(df, background)
                        else:
                            assert False, 'THIS SHOULD NEVER EXECUTE'
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
                                assert False, 'THIS SHOULD NEVER EXECUTE'
                                out_df = transform_matrix(prob_df, from_type='probability',
                                  to_type=to_type,
                                  background=background)
    out_df = validate_matrix(out_df)
    return out_df


def _counts_mat_to_probability_mat(counts_df, pseudocount=1.0):
    """
    Converts a counts matrix to a probability matrix
    """
    counts_df = validate_matrix(counts_df)
    check(pseudocount >= 0, 'pseudocount must be >= 0.')
    prob_df = counts_df.copy()
    vals = counts_df.values + pseudocount
    prob_df.loc[:, :] = vals / vals.sum(axis=1)[:, np.newaxis]
    prob_df = _normalize_matrix(prob_df)
    prob_df = validate_matrix(prob_df, matrix_type='probability')
    return prob_df


def _probability_mat_to_weight_mat(prob_df, background=None):
    """
    Converts a probability matrix to a weight matrix
    """
    prob_df = validate_matrix(prob_df, matrix_type='probability')
    bg_df = _get_background_mat(prob_df, background)
    weight_df = prob_df.copy()
    weight_df.loc[:, :] = np.log2(prob_df + SMALL) - np.log2(bg_df + SMALL)
    weight_df = validate_matrix(weight_df)
    return weight_df


def _weight_mat_to_probability_mat(weight_df, background=None):
    """
    Converts a weight matrix to a probability matrix
    """
    weight_df = validate_matrix(weight_df)
    bg_df = _get_background_mat(weight_df, background)
    prob_df = weight_df.copy()
    prob_df.loc[:, :] = bg_df.values * np.power(2, weight_df.values)
    prob_df = _normalize_matrix(prob_df)
    prob_df = validate_matrix(prob_df, matrix_type='probability')
    return prob_df


def _probability_mat_to_information_mat(prob_df, background=None):
    """
    Converts a probability matrix to an information matrix
    """
    prob_df = validate_matrix(prob_df, matrix_type='probability')
    bg_df = _get_background_mat(prob_df, background)
    info_df = prob_df.copy()
    fg_vals = prob_df.values
    bg_vals = bg_df.values
    tmp_vals = fg_vals * (np.log2(fg_vals + SMALL) - np.log2(bg_vals + SMALL))
    info_vec = tmp_vals.sum(axis=1)
    info_df.loc[:, :] = fg_vals * info_vec[:, np.newaxis]
    info_df = validate_matrix(info_df, matrix_type='information')
    return info_df


def _information_mat_to_probability_mat(info_df, background=None):
    """
    Converts an information matrix to an probability matrix
    """
    info_df = validate_matrix(info_df, matrix_type='information')
    bg_df = _get_background_mat(info_df, background)
    zero_indices = np.isclose(info_df.sum(axis=1), 0.0)
    info_df.loc[zero_indices, :] = bg_df.loc[zero_indices, :]
    prob_df = _normalize_matrix(info_df)
    prob_df = validate_matrix(prob_df, matrix_type='probability')
    return prob_df


def _normalize_matrix(df):
    """
    Normalizes a matrix df to a probability matrix prob_df
    """
    df = validate_matrix(df)
    check(all(df.values.ravel() >= 0), 'Some data frame entries are negative.')
    sums = df.sum(axis=1).values
    check(not any(np.isclose(sums, 0.0)), 'Some columns in df sum to nearly zero.')
    prob_df = df.copy()
    prob_df.loc[:, :] = df.values / sums[:, np.newaxis]
    prob_df = validate_matrix(prob_df, matrix_type='probability')
    return prob_df


def _center_matrix(df):
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
        the entries of the rows of out_df. Vector must be the same length
        as the number of columns in df
    3. background is a dataframe => it is then normalized and use as out_df.
        In this case, background must have the same rows and cols as df
    """
    num_pos, num_cols = df.shape
    bg_df = df.copy()
    if background is None:
        bg_df.loc[:, :] = 1 / num_cols
    else:
        if isinstance(background, (np.ndarray, list, tuple)):
            background = np.array(background)
            check(len(background) == num_cols, 'df and background have mismatched dimensions.')
            bg_df.loc[:, :] = background[np.newaxis, :]
            bg_df = _normalize_matrix(bg_df)
        else:
            if isinstance(background, pd.core.frame.DataFrame):
                bg_df = validate_matrix(background)
                check(all(df.index == bg_df.index), 'Error: df and bg_mat have different indexes.')
                check(all(df.columns == bg_df.columns), 'Error: df and bg_mat have different columns.')
                bg_df = _normalize_matrix(bg_df)
    bg_df = validate_matrix(bg_df, matrix_type='probability')
    return bg_df


@handle_errors
def alignment_to_matrix(sequences, counts=None, to_type='counts', background=None, characters_to_ignore='.-', center_weights=False, pseudocount=1.0):
    """
    Generates matrix from a sequence alignment

    parameters
    ----------
    sequences: (list of strings)
        A list of sequences, all of which must be the same length

    counts: (None or list of numbers)
        If not None, must be a list of numbers the same length os sequences,
        containing the (nonnegative) number of times that each sequence was
        observed. If None, defaults to 1.

    to_type: (str)
        The type of matrix to output. Must be 'counts', 'probability',
        'weight', or 'information'

    background: (array, or df)
        Specification of background probabilities. If array, should be the
        same length as df.columns and correspond to the probability of each
        column's character. If df, should be a probability matrix the same
        shape as df.

    characters_to_ignore: (str)
        Characters to ignore within sequences. This is often needed when
        creating matrices from gapped alignments.

    center_weights: (bool)
        Whether to subtract the mean of each row, but only if to_type=='weight'.

    pseudocount: (number >= 0.0)
        Pseudocount to use when converting from counts to probabilities.

    returns
    -------
    out_df: (dataframe)
        A matrix of the requested type.
    """
    check(isinstance(sequences, (list, tuple, np.ndarray, pd.Series)), 'sequences must be a list, tuple, np.ndarray, or pd.Series.')
    sequences = list(sequences)
    check(len(sequences) > 0, 'sequences must have length > 0.')
    check(all(isinstance(seq, str) for seq in sequences), 'sequences must all be of type string')
    check(isinstance(characters_to_ignore, str), 'type(seq) = %s must be of type str' % type(characters_to_ignore))
    check(isinstance(center_weights, bool), 'type(center_weights) = %s; must be bool.' % type(center_weights))
    L = len(sequences[0])
    check(all([len(s) == L for s in sequences]), 'all elements of sequences must have the same length.')
    check(isinstance(counts, (list, tuple, np.ndarray, pd.Series)) or counts is None, 'counts must be None or a list, tuple, np.ndarray, or pd.Series.')
    if counts is None:
        counts = np.ones(len(sequences))
    else:
        check(len(counts) == len(sequences), 'counts must be the same length as sequences;len(counts) = %d; len(sequences) = %d' % (
         len(counts), len(sequences)))
    check(isinstance(background, (type([]), np.ndarray, pd.DataFrame)) or background is None, 'type(background) = %s must be None or array-like or a dataframe.' % type(background))
    valid_types = MATRIX_TYPES.copy()
    check(to_type in valid_types, 'to_type=%s; must be in %s' % (to_type, valid_types))
    char_array = np.array([np.array(list(seq)) for seq in sequences])
    unique_characters = np.unique(char_array.ravel())
    unique_characters.sort()
    columns = [c for c in unique_characters if c not in characters_to_ignore]
    index = list(range(L))
    counts_df = pd.DataFrame(data=0, columns=columns, index=index)
    for c in columns:
        tmp_mat = (char_array == c).astype(float) * counts[:, np.newaxis]
        counts_df.loc[:, c] = tmp_mat.sum(axis=0).T

    out_df = transform_matrix(counts_df, from_type='counts',
      to_type=to_type,
      pseudocount=pseudocount,
      background=background)
    if center_weights:
        if to_type == 'weight':
            out_df = transform_matrix(out_df, center_values=True)
    return out_df


@handle_errors
def sequence_to_matrix(seq, cols=None, alphabet=None, is_iupac=False, to_type='probability', center_weights=False):
    """
    Generates a matrix from a sequence. With default keyword arguments,
    this is a one-hot-encoded version of the sequence provided. Alternatively,
    is_iupac=True allows users to get matrix models based in IUPAC motifs.

    parameters
    ----------

    seq: (str)
        Sequence from which to construct matrix.

    cols: (str or array-like or None)
        The characters to use for the matrix columns. If None, cols is
        constructed from the unqiue characters in seq. Overriden by alphabet
        and is_iupac.

    alphabet: (str or None)
        The alphabet used to determine the columns of the matrix.
        Options are: 'dna', 'rna', 'protein'. Ignored if None. Overrides cols.

    is_iupac: (bool)
        If True, it is assumed that the sequence represents an IUPAC DNA
        string. In this case, cols is overridden, and alphabet must be None.

    to_type: (str)
        The type of matrix to output. Must be 'probability', 'weight',
        or 'information'

    center_weights: (bool)
        Whether to subtract the mean of each row, but only if to_type='weight'.

    returns
    -------
    seq_df: (dataframe)
        the matrix returned to the user.
    """
    valid_types = MATRIX_TYPES.copy()
    valid_types.remove('counts')
    check(isinstance(seq, str), 'type(seq) = %s must be of type str' % type(seq))
    check(isinstance(center_weights, bool), 'type(center_weights) = %s; must be bool.' % type(center_weights))
    if cols is None:
        cols = list(set(seq))
        cols.sort()
    else:
        cols_types = (str, list, set, np.ndarray)
        check(isinstance(cols, cols_types), 'cols = %s must be None or a string, set, list, or np.ndarray')
    if alphabet is not None:
        valid_alphabets = list(ALPHABET_DICT.keys())
        check(alphabet in valid_alphabets, 'alphabet = %s; must be in %s.' % (alphabet, valid_alphabets))
        cols = list(ALPHABET_DICT[alphabet])
    else:
        check(to_type in valid_types, 'invalid to_type=%s; to_type must be in %s' % (to_type, valid_types))
        check(isinstance(is_iupac, bool), 'type(is_iupac) = %s; must be bool.' % type(is_iupac))
        if is_iupac:
            check(alphabet is None, 'must have alphabet=None if is_iupac=True')
            cols = list(ALPHABET_DICT['dna'])
        L = len(seq)
        index = list(range(L))
        counts_df = pd.DataFrame(data=0.0, columns=cols, index=index)
        if is_iupac:
            iupac_characters = list(IUPAC_DICT.keys())
            for i, c in enumerate(seq):
                check(c in iupac_characters, 'character %s at position %d is not a valid IUPAC character;must be one of %s' % (
                 c, i, iupac_characters))
                bs = IUPAC_DICT[c]
                for b in bs:
                    counts_df.loc[(i, b)] = 1.0

        else:
            for i, c in enumerate(seq):
                check(c in cols, 'character %s at position %d is not in cols=%s' % (
                 c, i, cols))
                counts_df.loc[(i, c)] = 1.0

    out_df = transform_matrix(counts_df, pseudocount=0,
      from_type='counts',
      to_type=to_type)
    if center_weights:
        if to_type == 'weight':
            out_df = transform_matrix(out_df, center_values=True)
    return out_df


@handle_errors
def saliency_to_matrix(seq, values, cols=None, alphabet=None):
    """
    Takes a sequence string and an array of values values and outputs a
    values dataframe. The returned dataframe is a L by C matrix where C is
    the number ofcharacters and L is sequence length.  If matrix is denoted as
    S, i indexes positions and c indexes characters, then S_ic will be non-zero
    (equal to the value in the values array at position p) only if character c
    occurs at position p in sequence. All other elements of S are zero.

    example usage:

    saliency_mat = logomaker.saliency_to_matrix(sequence,values)
    logomaker.Logo(saliency_mat)

    parameters
    ----------

    seq: (str or array-like list of single characters)
        sequence for which values matrix is constructed

    values: (array-like list of numbers)
        array of values values for each character in sequence

    cols: (str or array-like or None)
        The characters to use for the matrix columns. If None, cols is
        constructed from the unqiue characters in seq. Overridden by alphabet
        and is_iupac.

    alphabet: (str or None)
        The alphabet used to determine the columns of the matrix.
        Options are: 'dna', 'rna', 'protein'. Ignored if None. Overrides cols.

    returns
    -------
    saliency_df: (dataframe)
        values matrix in the form of a dataframe

    """
    if isinstance(seq, (list, np.ndarray, pd.Series)):
        try:
            seq = ''.join([str(x) for x in seq])
        except:
            check(False, 'could not convert %s to type str' % repr(str))

    else:
        try:
            seq = str(seq)
        except:
            check(False, 'could not convert %s to type str' % repr(str))

        check(isinstance(seq, str), 'type(seq) = %s must be of type str' % type(seq))
        check(isinstance(values, (type([]), np.ndarray, pd.Series)), 'type(values) = %s must be of type list' % type(values))
        values = list(values)
        check(len(seq) == len(values), 'length of seq and values list must be equal.')
        if cols is None:
            cols = list(set(seq))
            cols.sort()
        else:
            cols_types = (str, list, set, np.ndarray)
            check(isinstance(cols, cols_types), 'cols = %s must be None or a string, set, list, or np.ndarray')
            check(len(set(cols)) == len(set(seq)), 'length of set of unique characters must be equal for "cols " and "seq"')
            check(set(cols) == set(seq), 'unique characters for "cols" and "seq" must be equal.')
        if alphabet is not None:
            valid_alphabets = list(ALPHABET_DICT.keys())
            check(alphabet in valid_alphabets, 'alphabet = %s; must be in %s.' % (alphabet, valid_alphabets))
            cols = list(ALPHABET_DICT[alphabet])
        ohe_sequence = sequence_to_matrix(seq, cols=cols)
        saliency_df = ohe_sequence.copy()
        saliency_df.loc[:, :] = ohe_sequence.values * np.array(values)[:, np.newaxis]
        return saliency_df