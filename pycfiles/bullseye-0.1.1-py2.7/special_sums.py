# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bullseye/special_sums.py
# Compiled at: 2012-03-02 05:34:47
import numpy as np

def angle_sum(m, angle, aspect=1.0, binsize=None):
    r"""Compute the sum of a 2D array along an rotated axis.

    Parameters
    ----------
    m : array_like, shape(N, M)
        2D input array to be summed
    angle : float
        The angle of the summation direction defined such that:
            angle_sum(m, angle=0) == np.sum(m, axis=0)
            angle_sum(m, angle=np.pi/2) == np.sum(m, axis=1)
    aspect : float, optional
        The input bin aspect ratio (second dimension/first dimension).
    binsize : float, optional
        The output bin size in units of the first input dimension step
        size. If no binsize is given, it defaults to the "natural bin
        size" which is the larger projection of the two input step sizes
        onto the output dimension (the axis perpendicular to the
        summation axis).

    Returns
    -------
    out : ndarray, shape(K)
        The sum of `m` along the axis at `angle`.

    See also
    --------
    polar_sum : similar method summing azimuthally or radially

    Notes
    -----
    The summation angle is relative to the first dimension.

    For 0<=angle<=pi/2 the value at [0,0] ends up in the first bin and
    the value at [-1,-1] ends up in the last bin. Up to rounding, the
    center value will always end up in the center bin.

    For angle=3/4*pi the summation is along the diagonal.
    For angle=3/4*pi the summation is along the antidiagonal.
   
    The origin of the rotation is the [0,0] index. This determines the
    bin rounding.

    Up to index flipping, limits, rounding, offset and the definition of
    `angle` the output `o` is:

    .. math::
      o_k = \sum_l m_{i,j/a}, where
      i(l,k) = \cos(\alpha) l - \sin(\alpha) k
      j(l,k) = \sin(\alpha) l + \cos(\alpha) k

    There is no interpolation and artefacts are likely if this function
    is interpreted as an image processing function.

    The full array sum is always strictly conserved:
        angle_sum(m, t).sum() == m.sum()

    The function uses floor(coordinate+.5) to bin (c.f. around, rint,
    trunc).

    Examples
    --------
    >>> m = np.arange(9.).reshape((3, 3))
    >>> np.all(angle_sum(m, 0) == m.sum(axis=0))
    True
    >>> np.all(angle_sum(m, np.pi/2) == m.sum(axis=1))
    True
    >>> np.all(angle_sum(m, np.pi) == m.sum(axis=0)[::-1])
    True
    >>> np.all(angle_sum(m, 3*np.pi/2) == m.sum(axis=1)[::-1])
    True
    >>> np.all(angle_sum(m, 2*np.pi) == m.sum(axis=0))
    True
    >>> np.all(angle_sum(m, -np.pi/2) == 
    ...        angle_sum(m, 3*np.pi/2))
    True
    >>> d1 = np.array([0, 4, 12, 12, 8]) # antidiagonal
    >>> d2 = np.array([2, 6, 12, 10, 6]) # diagonal
    >>> np.all(angle_sum(m, np.pi/4) == d1)
    True
    >>> np.all(angle_sum(m, 3*np.pi/4) == d2)
    True
    >>> np.all(angle_sum(m, 5*np.pi/4) == d1[::-1])
    True
    >>> np.all(angle_sum(m, 7*np.pi/4) == d2[::-1])
    True
    >>> np.all(angle_sum(m, 0, aspect=2, binsize=1) == 
    ...        np.array([9, 0, 12, 0, 15]))
    True
    >>> np.all(angle_sum(m, 0, aspect=.5, binsize=1) == 
    ...        np.array([9, 12+15]))
    True
    >>> np.all(angle_sum(m, 0, aspect=.5) == m.sum(axis=0))
    True
    >>> np.all(angle_sum(m, np.pi/2, aspect=2, binsize=1) ==
    ...        m.sum(axis=1))
    True
    >>> m2 = np.arange(1e6).reshape((100, 10000))
    >>> np.all(angle_sum(m2, 0) == m2.sum(axis=0))
    True
    >>> np.all(angle_sum(m2, np.pi/2) == m2.sum(axis=1))
    True
    >>> angle_sum(m2, np.pi/4).shape
    (10099,)
    >>> angle_sum(m2, np.pi/4).sum() == m2.sum()
    True
    """
    m = np.atleast_2d(m)
    if binsize is None:
        binsize = max(abs(np.cos(angle) * aspect), abs(np.sin(angle)))
    m = m[::-1]
    i, j = np.ogrid[:m.shape[0], :m.shape[1]]
    k = np.cos(angle) * aspect / binsize * j - np.sin(angle) / binsize * i
    cx, cy = (0, 0, -1, -1), (0, -1, 0, -1)
    km = k[(cx, cy)].min()
    k = np.floor(k - (km - 0.5)).astype(np.int)
    return np.bincount(k.ravel(), m.ravel())


def polar_sum(m, center, direction, aspect=1.0, binsize=None):
    """Compute the sum of a 2D array radially or azimuthally.

    Parameters
    ----------
    m : array_like, shape(N, M)
        2D input array to be summed
    center : tuple(float, float)
        The center of the summation measured from the [0, 0] index
        in units of the two input step sizes.
    direction : "radial" or "azimuthal"
        Summation direction.
    aspect : float, optional
        The input bin aspect ratio (second dimension/first dimension).
    binsize : int, optional
        The output bin size. If None is given, and direction="radial"
        then binsize=2*pi/100, else binsize=min(1, aspect).

    Returns
    -------
    out : ndarray, shape(K)
        The radial or azimuthal sum of `m`.

    See also
    --------
    angle_sum : similar method summing along angled parallel lines

    Notes
    -----
    The index of `out` is the floor()-binned radius or the floor()
    binned angle, both according to `binsize`.

    Angles are measured from the positive second index axis towards the
    negative first index axis. They correspond to mathematically
    positive angles in the index coordinates of m[::-1] -- or the [0, 0]
    index in the lower left.

    If direction="azimuthal" then the length of the output is determined
    by the maximal distance to the center. The radius-bins are [0, binsize),
    [binsize, 2*binsize), ... up to [r, r+binsize) for
    some value r with max_radius-binsize <= r < max_radius.
    
    If direction="radial" the length is always 2*pi/binsize. This is not
    the same as arctan2(i, j) which would distinguish +pi and -pi!
    The azimuthal bins are therefore [-pi, -pi+binsize),
    [-pi+binsize, 2*binsize), ... up to [p-binsize, p) for some p with 
    pi-binsize <= p < pi. The values at +pi end up in the first bin.
    See arctan2() for the definition of the behaviour other special
    cases.

    There is no interpolation and artefacts are likely if this function
    is interpreted as an image processing function.

    The full array sum is always strictly conserved:
        polar_sum(m, ...).sum() == m.sum()

    The function uses (coordinate).astype(np.int) to bin.

    Examples
    --------
    >>> m = np.arange(1., 10.).reshape((3, 3))
    >>> polar_sum(m, (0, 0), "radial").sum() == m.sum()
    True
    >>> polar_sum(m, (0, 0), "azimuthal").sum() == m.sum()
    True
    >>> polar_sum(m, (1, 1), "radial").sum() == m.sum()
    True
    >>> polar_sum(m, (1, 1), "azimuthal").sum() == m.sum()
    True
    >>> polar_sum(m, (1, 1), "radial", binsize=np.pi/4)
    array([  4.,   1.,   2.,   3.,  11.,   9.,   8.,   7.])
    >>> polar_sum(m, (1, 1), "azimuthal", binsize=1.)
    array([  5.,  40.])
    >>> polar_sum(m, (1, 1), "azimuthal", binsize=2**.5/2)
    array([  5.,  20.,  20.])
    >>> polar_sum(m, (.5, .5), "azimuthal", binsize=1)
    array([ 12.,  24.,   9.])
    >>> polar_sum(m, (0, 0), "radial", binsize=np.pi/8)
    array([  0.,   0.,   0.,   0.,   0.,   0.,   0.,   0.,   6.,   6.,  22.,
             0.,  11.,   0.,   0.,   0.])
    >>> polar_sum(m, (0, 0), "radial", binsize=np.pi/2)
    array([  0.,   0.,  34.,  11.])
    >>> m2 = np.arange(123*345).reshape((123, 345))
    >>> polar_sum(m2, (67, 89), "radial", binsize=2*np.pi/1011).shape[0]
    1011
    """
    m = np.atleast_2d(m)
    i, j = np.ogrid[:m.shape[0], :m.shape[1]]
    i, j = i - center[0], j - center[1]
    if direction == 'azimuthal':
        k = (j ** 2 * aspect ** 2 + i ** 2) ** 0.5
        if binsize is None:
            binsize = min(1.0, aspect)
        minlength = None
    elif direction == 'radial':
        k = np.arctan2(i, j * aspect) + np.pi
        if binsize is None:
            binsize = 2 * np.pi / 100
        minlength = int(2 * np.pi / binsize) + 1
    else:
        raise ValueError("direction needs to be 'radial' or 'azimuthal'")
    k = (k / binsize).astype(np.int)
    r = np.bincount(k.ravel(), m.ravel(), minlength)
    if direction == 'radial':
        assert r.shape[0] == minlength, (r.shape, minlength)
        r[0] += r[(-1)]
        r = r[:-1]
    return r


if __name__ == '__main__':
    import doctest
    doctest.testmod()