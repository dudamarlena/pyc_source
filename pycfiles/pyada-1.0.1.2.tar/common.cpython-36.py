# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tad/influxexample/pyad/pyad/pyad/common.py
# Compiled at: 2019-01-28 15:55:55
# Size of source mod 2**32: 6651 bytes
import numpy as np, logging
logger = logging.getLogger(__name__)
NA = np.nan

def nrow(x):
    if len(x.shape) == 2:
        return x.shape[0]


def ncol(x):
    if len(x.shape) == 2:
        return x.shape[1]


def rbind(m1, m2):
    if m1 is None:
        return np.copy(m2)
    else:
        return np.append(m1, m2, axis=0)


def cbind(m1, m2):
    if len(m1.shape) == 1:
        if len(m2.shape) == 1:
            if len(m1) == len(m2):
                mat = np.empty(shape=(len(m1), 2))
                mat[:, 0] = m1
                mat[:, 1] = m2
                return mat
            raise ValueError('length of arrays differ: (%d, %d)' % (len(m1), len(m2)))
    return np.append(m1, m2, axis=1)


def matrix(d, nrow=None, ncol=None, byrow=False):
    """Returns the data as a 2-D matrix

    A copy of the same matrix will be returned if input data dimensions are
    same as output data dimensions. Else, a new matrix will be created
    and returned.

    Example:
        d = np.reshape(range(12), (6, 2))
        matrix(d[0:2, :], nrow=2, byrow=True)

    Args:
        d:
        nrow:
        ncol:
        byrow:

    Returns: np.ndarray
    """
    if byrow:
        order = 'C'
    else:
        order = 'F'
    if len(d.shape) == 2:
        d_rows, d_cols = d.shape
    else:
        if len(d.shape) == 1:
            d_rows, d_cols = 1, d.shape[0]
        else:
            raise ValueError('Dimensions more than 2 are not supported')
    if nrow is not None:
        if ncol is None:
            ncol = int(d_rows * d_cols / float(nrow))
    if ncol is not None:
        if nrow is None:
            nrow = int(d_rows * d_cols / float(ncol))
    if len(d.shape) == 2:
        if d_rows == nrow:
            if d_cols == ncol:
                return d.copy()
    if not d_rows * d_cols == nrow * ncol:
        raise ValueError('input dimensions (%d, %d) not compatible with output dimensions (%d, %d)' % (
         d_rows, d_cols, nrow, ncol))
    if isinstance(d, csr_matrix):
        return d.reshape((nrow, ncol), order=order)
    else:
        return np.reshape(d, (nrow, ncol), order=order)


def order(x, decreasing=False):
    if decreasing:
        return np.argsort(-x)
    else:
        return np.argsort(x)


def sample(x, n):
    shuffle = np.array(x)
    np.random.shuffle(shuffle)
    return shuffle[0:n]


def histogram_r(x, g1=1.0, g2=1.0, g3=-1.0, verbose=False):
    """Construct histograms that mimic behavior of R histogram package

    The type of histogram is 'regular', and right-open
    Note: the number of breaks is being computed as in:
    L. Birge, Y. Rozenholc, How many bins should be put in a regular histogram? 2006
    """
    n = len(x)
    nbinsmax = int(g1 * n ** g2 * np.log(n) ** g3)
    if verbose:
        logger.debug('max bins: %d' % (nbinsmax,))
    y = np.sort(x)
    likelihood = np.zeros(nbinsmax, dtype=float)
    pen = np.arange(1, (nbinsmax + 1), dtype=float) + np.log(np.arange(1, (nbinsmax + 1), dtype=float)) ** 2.5
    for d in range(1, nbinsmax + 1):
        counts, breaks = np.histogram(x, bins=d, density=False)
        density = counts / (n * (breaks[1] - breaks[0]))
        like = np.zeros(d, dtype=float)
        like2 = np.zeros(d, dtype=float)
        tmp = np.where(counts > 0)[0]
        if len(tmp) > 0:
            like2[tmp] = np.log(density[tmp])
        like[np.isfinite(like2)] = like2[np.isfinite(like2)]
        likelihood[d - 1] = np.sum(counts * like)
        if np.min(counts) < 0:
            likelihood[d - 1] = -np.Inf

    penlike = likelihood - pen
    optd = np.argmax(penlike)
    if verbose:
        logger.debug('optimal num bins: %d' % (optd + 1,))
    counts, breaks = np.histogram(x, bins=(optd + 1), density=False)
    density = counts / (n * (breaks[1] - breaks[0]))
    hist = HistogramR(counts=(np.array(counts, float)), density=(np.array(density, float)), breaks=np.array(breaks, dtype=float))
    return hist


def pdf_hist_equal_bins(x, h, minpdf=1e-08):
    p = (x - h.breaks[0]) / (h.breaks[1] - h.breaks[0])
    ndensity = len(h.density)
    p = np.array([min(int(np.trunc(v)), ndensity - 1) for v in p])
    d = h.density[p]
    d = np.array([max(v, minpdf) for v in d])
    return d