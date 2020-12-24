# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: mpathic/src/numerics.py
# Compiled at: 2018-06-21 15:19:21
import time
from mpathic.src import simulate_library
from setuptools import Extension
fast = Extension('fast', ['fast.c'])
from mpathic.src import qc
from mpathic.src.profile_mut import ProfileMut
from mpathic.src.simulate_library import SimulateLibrary
import numpy as np
from scipy.sparse import csr, csr_matrix, lil_matrix
from mpathic import SortSeqError
import pdb, sys
from mpathic.src import fast

def nbytes(array):
    if isinstance(array, np.ndarray):
        return array.nbytes
    else:
        if isinstance(array, csr.csr_matrix):
            return array.data.nbytes + array.indptr.nbytes + array.indices.nbytes
        return sizeof(array)


def dataset2seqarray(dataset_df, modeltype):
    if modeltype == 'MAT':
        seqs2array = fast.seqs2array_for_matmodel
    elif modeltype == 'NBR':
        seqs2array = fast.seqs2array_for_nbrmodel
    else:
        raise SortSeqError('Unknown model type: %s' % modeltype)
    seqcol = qc.get_cols_from_df(dataset_df, 'seqs')[0]
    seqtype = qc.colname_to_seqtype_dict[seqcol]
    seqlist = list(dataset_df[seqcol])
    seqarray = seqs2array(seqlist, seq_type=seqtype)
    return seqarray


def dataset2mutarray(dataset_df, modeltype, chunksize=1000, rowsforwtcalc=100):
    if modeltype == 'MAT':
        seqs2array = fast.seqs2array_for_matmodel
    else:
        if modeltype == 'NBR':
            seqs2array = fast.seqs2array_for_nbrmodel
        else:
            raise SortSeqError('Unknown model type: %s' % modeltype)
        seqcol = qc.get_cols_from_df(dataset_df, 'seqs')[0]
        seqtype = qc.colname_to_seqtype_dict[seqcol]
        wtcol = qc.seqtype_to_wtcolname_dict[seqtype]
        rowsforwtcalc = min(rowsforwtcalc, dataset_df.shape[0])
        dataset_head_df = dataset_df.head(rowsforwtcalc)
        mut_df = ProfileMut(dataset_df=dataset_head_df).mut_df
        wtseq = ('').join(list(mut_df[wtcol]))
        print wtseq
        wtrow = seqs2array([wtseq], seq_type=seqtype).ravel().astype(bool)
        numfeatures = len(wtrow)
        startrow = 0
        endrow = startrow + chunksize - 1
        numrows = dataset_df.shape[0]
        mutarray_lil = lil_matrix((numrows, numfeatures), dtype=int)
        matrix_filled = False
        while not matrix_filled:
            if startrow >= numrows:
                matrix_filled = True
                continue
            elif endrow >= numrows:
                endrow = numrows - 1
                matrix_filled = True
            seqlist = list(dataset_df[seqcol][startrow:endrow + 1])
            seqarray = seqs2array(seqlist, seq_type=seqtype)
            tmp = seqarray.copy()
            tmp[:, wtrow] = 0
            mutarray_lil[startrow:endrow + 1, :] = tmp
            startrow = endrow + 1
            endrow = startrow + chunksize - 1

    mutarray_csr = mutarray_lil.tocsr()
    return (
     mutarray_csr, wtrow)


def dataset2mutarray_withwtseq(dataset_df, modeltype, wtseq, chunksize=1000):
    if modeltype == 'MAT':
        seqs2array = fast.seqs2array_for_matmodel
    else:
        if modeltype == 'NBR':
            seqs2array = fast.seqs2array_for_nbrmodel
        else:
            raise SortSeqError('Unknown model type: %s' % modeltype)
        seqcol = qc.get_cols_from_df(dataset_df, 'seqs')[0]
        seqtype = qc.colname_to_seqtype_dict[seqcol]
        wtcol = qc.seqtype_to_wtcolname_dict[seqtype]
        wtrow = seqs2array([wtseq], seq_type=seqtype).ravel().astype(bool)
        numfeatures = len(wtrow)
        startrow = 0
        endrow = startrow + chunksize - 1
        numrows = dataset_df.shape[0]
        mutarray_lil = lil_matrix((numrows, numfeatures), dtype=int)
        matrix_filled = False
        while not matrix_filled:
            if startrow >= numrows:
                matrix_filled = True
                continue
            elif endrow >= numrows:
                endrow = numrows - 1
                matrix_filled = True
            seqlist = list(dataset_df[seqcol][startrow:endrow + 1])
            seqarray = seqs2array(seqlist, seq_type=seqtype)
            tmp = seqarray.copy()
            tmp[:, wtrow] = 0
            mutarray_lil[startrow:endrow + 1, :] = tmp
            startrow = endrow + 1
            endrow = startrow + chunksize - 1

    mutarray_csr = mutarray_lil.tocsr()
    return (
     mutarray_csr, wtrow)


def eval_modelmatrix_on_mutarray(modelmatrix, mutarray, wtrow):
    print (
     'numerics: sizes: ', modelmatrix.size, ' ', wtrow.size)
    if not isinstance(modelmatrix, np.ndarray):
        raise SortSeqError('modelmatrix is not a np.ndarray')
    if not isinstance(wtrow, np.ndarray):
        raise SortSeqError('wtrow is not an np.ndarray')
    if not isinstance(mutarray, csr.csr_matrix):
        raise SortSeqError('mutarray is not a sparse csr_matrix')
        raise SortSeqError('Unrecognized model type %s' % modeltype)
    if len(wtrow.shape) != 1:
        raise SortSeqError('wtrow is not 1-dimensional')
    if len(modelmatrix.shape) != 2:
        raise SortSeqError('modelmatrix is not 2-dimensional')
    if wtrow.size != modelmatrix.size:
        raise SortSeqError('wtrow does not match modelmatrix')
    modelmatrix_vec = modelmatrix.ravel()
    const_val = np.dot(wtrow, modelmatrix_vec)
    tmp_matrix = modelmatrix.copy()
    indices = wtrow.reshape(modelmatrix.shape).astype(bool)
    wt_matrix_vals = tmp_matrix[indices]
    tmp_matrix -= wt_matrix_vals[:, np.newaxis]
    modelmatrix_for_mutarray = csr_matrix(np.matrix(tmp_matrix.ravel()).T)
    mutarray_vals = mutarray * modelmatrix_for_mutarray
    vals = const_val + mutarray_vals.toarray().ravel()
    return vals