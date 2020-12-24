# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/paddle/common.py
# Compiled at: 2011-02-15 05:30:07
"""
Common or low-level private functions.
"""
import scipy as sp
from scipy import stats
from scipy import linalg as LA
import pylab
ra = sp.random

def _cost_rec(D, X, U, pars=None):
    r"""
    Reconstruction error term.

    Computes the normalized reconstruction error :math:`\|X-DU\|_F^2/(d*N)`.

    Parameters
    ----------
    D : (d, K) ndarray
        Dictionary.
    X : (d, N) ndarray
        Input data.
    U : (K, N) ndarray
        Encondings.
    pars : not used
    
    Returns
    -------
    rec_err : float
        Reconstruction error.
    """
    assert D.shape[1] == U.shape[0]
    assert X.shape[0] == D.shape[0]
    assert X.shape[1] == U.shape[1]
    return ((X - sp.dot(D, U)) ** 2).mean()


def _cost_cod(C, X, U, pars):
    r"""
    Coding error term.

    Computes the normalized and weighted coding error :math:`\eta\|U-CX\|_F^2/(K*N)`.

    Parameters
    ----------
    C : (K, d) ndarray
        Dual Dictionary.
    X : (d, N) ndarray
        Input data.
    U : (K, N) ndarray
        Encondings.
    pars : dict with at least key eta
        pars["eta"] is the :math:`\eta` parameter weighting the coding error
    
    Returns
    -------
    cod_err : float
        Coding error.
    """
    assert C.shape[0] == U.shape[0]
    assert X.shape[0] == C.shape[1]
    assert X.shape[1] == U.shape[1]
    assert pars['eta'] >= 0
    return pars['eta'] * ((U - sp.dot(C, X)) ** 2).mean()


def _replaceAtoms(X, U, D, replace):
    """
    Replaces some atoms.

    Replaces the atoms of ``D`` listed in ``replace`` with the worst
    reconstructed examples of ``X``.
    Only ``U`` is changed (and returned).

    Parameters
    ----------
    X : (d, N) ndarray
        Input data 
    U : (K, N) ndarray
        Current encodings of the input data X
    D : (d, K) ndarray
        Current dictionary
    replace : list of integer
        List of indexes of the atoms to be replaced
    
    Returns
    -------
    U : (K, N) ndarray
        The updated encodings.
    """
    r = sp.sum((X - sp.dot(D, U)) ** 2, 0) / sp.sum(X ** 2, 0)
    i = sp.argsort(r)[::-1]
    U[(replace, i[:len(replace)])] = 1
    return U


def _saveDict(D, U, Nrows=8, Ncols=25, path='./savedDict.png', sorted=False):
    """
    Saves a figure of a dictionary atoms.

    Creates a table with ``Nrows x Ncols`` images of the atoms of ``D``,
    drawn as square image patches.
    It assumes that the dimension ``d`` of the atoms is a perfect square.

    Parameters
    ----------
    D : (d, K) ndarray
        Dictionary
    U : (K, N) ndarray
        Encodings
    Nrows : integer
        Number of rows in the figure
    Ncols : integer
        Number of columns in the figure
    path : string
        Name of the file where the figure will be saved
    sorted : bool
        If True, the atoms will be sorted according to their usage in U
    """
    d = D.shape[0]
    W = sp.sqrt(d)
    assert Nrows * Ncols <= D.shape[1]
    if sorted:
        usage = sp.sum(sp.where(sp.absolute(U) > 1e-06, 1, 0), 1)
        order = sp.argsort(usage)[::-1]
        subset = order[:Nrows * Ncols]
    else:
        subset = sp.arange(0, Nrows * Ncols)
    D = D * sp.sign(sp.mean(D, 0)).reshape((1, -1))
    m = 2
    imgD = sp.ones((W * Nrows + m * (Nrows + 1), W * Ncols + m * (Ncols + 1)))
    vminD = stats.scoreatpercentile(D.flatten(), 2)
    vmaxD = stats.scoreatpercentile(D.flatten(), 98)
    imgD *= vmaxD
    for i in xrange(Ncols):
        for j in xrange(Nrows):
            k = i * Nrows + j
            if k == len(subset):
                break
            y, x = j * (W + m) + m, i * (W + m) + m
            imgD[y:y + W, x:x + W] = D[:, subset[k]].reshape((W, W))

        if k == len(subset):
            break

    dpi = 50.0
    pylab.figure(figsize=(imgD.shape[1] / dpi, imgD.shape[0] / dpi), dpi=dpi)
    pylab.imshow(imgD, interpolation='nearest', vmin=vminD, vmax=vmaxD)
    pylab.gray()
    pylab.xticks(())
    pylab.yticks(())
    pylab.savefig(path, dpi=300, bbox_inches='tight', transparent=True)
    return


def print_frame_assessment(D):
    r"""
    Prints an evalutation of D as a frame.

    This functions computes and prints the following information for :math:`D`:

    - the frame bounds (computed from the eigenvalues)

    - the equivalent tight frame constant :math:`\alpha`

    - if there is a violation of the fundamental inequality

    - the value of the frame potential and its theoretical lower bound

    - the relative error between the frame operator :math:`DD^T` and :math:`\alpha I`

    - the mutual coherence

    Parameters
    ----------
    D : (d, K) ndarray
        Frame matrix
    """
    (d, K) = D.shape
    ew = LA.eigvalsh(sp.dot(D, D.T))
    print ' frame bounds: A = %.2f and B = %.2f' % (ew.min(), ew.max())
    a = sp.sum(D ** 2, 0)
    A = a.sum() / d
    print ' assuming frame constant A = %.2f (K/d = %.2f)' % (A, float(K) / d)
    print ' max(|d_i|^2) = %.2f' % a.max()
    if a.max() > A:
        print '!! fundamental inequality violated !!'
        order = sp.argsort(a)[::-1]
        a = a[order]
        D = D[:, order]
        for i in xrange(len(a)):
            if a[i] <= a[i + 1:].sum() / (d - i - 1):
                break

        lbound = (a[:i] ** 2).sum() + 1 / (d - i) * a[i:].sum() ** 2
    else:
        lbound = a.sum() ** 2 / d
    print ' theoretical lower bound for a TF is %f' % lbound
    print ' frame potential = %f' % (sp.dot(D.T, D) ** 2).sum()
    Id = A * sp.identity(d)
    print ' rel. error between DDt and AI = %.2f' % (LA.norm(Id - sp.dot(D, D.T)) / LA.norm(Id))
    print ' Mutual coherence = %.3f' % coherence(D)


def coherence(D):
    """
    Compute the mutual coherence of D.

    Parameters
    ----------
    D : (d, K) ndarray
        A dictionary.

    Returns
    -------
    c : float
        The mutual coherence.
    """
    (d, K) = D.shape
    n = sp.sqrt(sp.sum(D ** 2, 0)).reshape((1, -1))
    mc = sp.dot(D.T, D) / (n * n.T)
    mc[(sp.arange(K), sp.arange(K))] = 0
    return mc.max()


def cumcoherence(D, C=None):
    """
    Compute the cumulative mutual/cross coherence of D/(D,C).

    Parameters
    ----------
    D : (d, K) ndarray
        A dictionary.
    C : (K, d) ndarray
        A dual of the dictionary (optional).

    Returns
    -------
    c : (K-1,) ndarray
        The cumulative coherence.
    """
    if C == None:
        C = D.T
    assert C.shape == D.T.shape, C.shape
    D = D / sp.sqrt(sp.sum(D ** 2, 0)).reshape((1, -1))
    C = C / sp.sqrt(sp.sum(C ** 2, 1)).reshape((-1, 1))
    coh = sp.absolute(sp.dot(D.T, C.T))
    (d, K) = D.shape
    coh[(sp.arange(K), sp.arange(K))] = 0
    coh = sp.sort(coh, 1)
    coh = sp.add.accumulate(coh[:, ::-1], 1)
    return sp.max(coh, 0)


def img2patches(img, size, Nmax=0):
    """
    Extract patches from an image.

    Parameters
    ----------
    img : (rows, cols) or (rows, cols, channels) ndimage
        Input image.
    size : 2-tuple
        Size of the patches
    Nmax : int
        If > 0, number of patches to sample randomly
    """
    assert img.ndim == 2, img.shape
    (H, W) = img.shape
    assert len(size) == 2, size
    (h, w) = size
    n = (H - h) * (W - w)
    yx = sp.indices((H - h, W - w)).reshape((2, -1, 1))
    assert yx.shape == (2, n, 1), yx.shape
    if Nmax > 0:
        yx = yx[:, ra.permutation(n)[:Nmax]]
        n = Nmax
    stencil = sp.indices(size)
    stencil.shape = (2, 1, -1)
    s = stencil + yx
    assert s.shape == (2, n, h * w), s.shape
    p = img[(s[0], s[1])]
    assert p.shape == (n, h * w), p.shape
    return p.T


def sparsity(X, axis=0):
    assert X.ndim <= 2, X.shape
    assert axis <= X.ndim, axis
    r = sp.sum(sp.absolute(X), axis) / sp.sqrt(sp.sum(X ** 2, axis))
    sqrtn = sp.sqrt(X.shape[axis])
    return (sqrtn - r) / (sqrtn - 1)


def gendata(d, N, s, K, D=None):
    """
    Generates N vectors in d dimensions. Each vector is the linear
    combinations of s atoms sampled from a dictionary of size K.
    """
    if D == None:
        D0 = sp.random.normal(size=(d, K))
    else:
        assert D.shape[0] == d, D.shape
        assert D.shape[1] >= K, D.shape
        D0 = D[:, :K]
    D0 /= sp.sqrt(sp.sum(D0 ** 2, 0)).reshape((1, -1))
    U = sp.zeros((K, N))
    for i in xrange(N):
        j = sp.random.permutation(U.shape[0])[:s]
        U[(j, i)] = sp.random.normal(size=(s,))

    X = sp.dot(D0, U)
    return (X, D0, U)