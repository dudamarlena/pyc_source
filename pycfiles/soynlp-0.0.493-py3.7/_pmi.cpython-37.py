# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/soynlp/word/_pmi.py
# Compiled at: 2019-02-17 12:57:44
# Size of source mod 2**32: 5344 bytes
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse import diags
from scipy.sparse import dok_matrix
from sklearn.metrics import pairwise_distances
from soynlp.utils import get_process_memory
from soynlp.vectorizer import sent_to_word_contexts_matrix

def _as_diag(px, alpha):
    px_diag = diags(px.tolist()[0])
    px_diag.data[0] = np.asarray([0 if v == 0 else 1 / (v + alpha) for v in px_diag.data[0]])
    return px_diag


def _logarithm_and_ppmi(exp_pmi, min_exp_pmi):
    n, m = exp_pmi.shape
    rows, cols = exp_pmi.nonzero()
    data = exp_pmi.data
    indices = np.where(data >= min_exp_pmi)[0]
    rows = rows[indices]
    cols = cols[indices]
    data = data[indices]
    data = np.log(data)
    exp_pmi_ = csr_matrix((data, (rows, cols)), shape=(n, m))
    return exp_pmi_


def pmi(X, py=None, min_pmi=0, alpha=0.0, beta=1):
    """
    :param X: scipy.sparse.csr_matrix
        (word, contexts) sparse matrix
    :param py: numpy.ndarray
        (1, word) shape, probability of context words.
    :param min_pmi: float
        Minimum value of pmi. all the values that smaller than min_pmi
        are reset to zero.
        Default is zero.
    :param alpha: float
        Smoothing factor. pmi(x,y; alpha) = p_xy /(p_x * (p_y + alpha))
        Default is 0.0
    :param beta: float
        Smoothing factor. pmi(x,y) = log ( Pxy / (Px x Py^beta) )
        Default is 1.0

    Returns
    ----------
    pmi : scipy.sparse.csr_matrix
        (word, contexts) pmi value sparse matrix
    px : numpy.ndarray
        Probability of rows (items)
    py : numpy.ndarray
        Probability of columns (features)

    Usage
    -----
        >>> pmi, px, py = pmi_memory_friendly(X, py=None, min_pmi=0, alpha=0, beta=1.0)
    """
    assert 0 < beta <= 1
    px = np.asarray((X.sum(axis=1) / X.sum()).reshape(-1))
    if py is None:
        py = np.asarray((X.sum(axis=0) / X.sum()).reshape(-1))
    if beta < 1:
        py = py ** beta
        py /= py.sum()
    pxy = X / X.sum()
    px_diag = _as_diag(px, 0)
    py_diag = _as_diag(py, alpha)
    exp_pmi = px_diag.dot(pxy).dot(py_diag)
    min_exp_pmi = 1 if min_pmi == 0 else np.exp(min_pmi)
    pmi = _logarithm_and_ppmi(exp_pmi, min_exp_pmi)
    return (
     pmi, px, py)


def pmi_memory_friendly(X, py=None, min_pmi=0, alpha=0.0, beta=1.0, verbose=False):
    """
    :param X: scipy.sparse.csr_matrix
        (word, contexts) sparse matrix
    :param py: numpy.ndarray
        (1, word) shape, probability of context words.
    :param min_pmi: float
        Minimum value of pmi. all the values that smaller than min_pmi
        are reset to zero.
        Default is zero.
    :param alpha: float
        Smoothing factor. pmi(x,y; alpha) = p_xy /(p_x * (p_y + alpha))
        Default is 0.0
    :param beta: float
        Smoothing factor. pmi(x,y) = log ( Pxy / (Px x Py^beta) )
        Default is 1.0
    :param verbose: Boolean
        If True, verbose mode on

    Returns
    ----------
    pmi : scipy.sparse.dok_matrix
        (word, contexts) pmi value sparse matrix
    px : numpy.ndarray
        Probability of rows (items)
    py : numpy.ndarray
        Probability of columns (features)

    Usage
    -----
        >>> pmi, px, py = pmi_memory_friendly(X, py=None, min_pmi=0, alpha=0, beta=1.0)
    """
    assert 0 < beta <= 1
    px = (X.sum(axis=1) / X.sum()).reshape(-1)
    if py is None:
        py = (X.sum(axis=0) / X.sum()).reshape(-1)
    pxy = X / X.sum()
    assert py.shape[0] == pxy.shape[1]
    if beta < 1:
        py = py ** beta
        py /= py.sum()
    px_diag = diags(px.tolist()[0])
    py_diag = diags(py.tolist()[0])
    px_diag.data[0] = np.asarray([0 if v == 0 else 1 / v for v in px_diag.data[0]])
    py_diag.data[0] = np.asarray([0 if v == 0 else 1 / (v + alpha) for v in py_diag.data[0]])
    exp_pmi = px_diag.dot(pxy).dot(py_diag)
    min_exp_pmi = 1 if min_pmi == 0 else np.exp(min_pmi)
    indices = np.where(exp_pmi.data > min_exp_pmi)[0]
    pmi_dok = dok_matrix(exp_pmi.shape)
    rows, cols = exp_pmi.nonzero()
    data = exp_pmi.data
    for _n_idx, idx in enumerate(indices):
        if verbose:
            if _n_idx % 10000 == 0:
                print(('\rcomputing pmi {:.3} %  mem={} Gb    '.format(100 * _n_idx / indices.shape[0], '%.3f' % get_process_memory())),
                  flush=True,
                  end='')
        pmi_dok[(rows[idx], cols[idx])] = np.log(data[idx])

    if verbose:
        print(('\rcomputing pmi was done{}'.format('                              ')), flush=True)
    return (pmi_dok, px, py)