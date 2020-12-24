# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/lapack_dsyevd.py
# Compiled at: 2007-08-13 06:22:59
import lapack_dsy, Numeric

def _lg(n):
    k = 0
    twok = 1
    while twok < n:
        k += 1
        twok *= 2

    return k


def dsyevd(a, jobz='V', uplo='U'):
    """Eigenvalues and eigenvectors of a real symmetric matrix."""
    if jobz != 'V':
        jobz = 'N'
    a = Numeric.array(a, Numeric.Float)
    n = a.shape[0]
    assert a.shape == (n, n)
    eval = Numeric.zeros((n,), Numeric.Float)
    work = Numeric.zeros((1 + 5 * n + 2 * n * _lg(n) + 3 * n * n,), Numeric.Float)
    iwork = Numeric.zeros((2 * (2 + 5 * n),), Numeric.Int)
    info = 0
    o = lapack_dsy.dsyevd(jobz, uplo, n, a, n, eval, work, len(work), iwork, len(iwork), info)
    assert o['info'] == 0
    if jobz != 'V':
        a = None
    return (
     eval, a)


def _err(a):
    return Numeric.sum(a ** 2)


def _asdiagonal(a):
    n = a.shape[0]
    return Numeric.identity(n) * a


def _reconstruct(eval, evec):
    x = Numeric.matrixmultiply(Numeric.transpose(a2), Numeric.matrixmultiply(_asdiagonal(ev2), a2))
    return x


if __name__ == '__main__':
    i = Numeric.array([[2, 0], [0, 1]], Numeric.Float)
    print dsyevd(i)
    import RandomArray
    i = RandomArray.random((4, 4)) + 1 * Numeric.identity(4)
    i = i + Numeric.transpose(i)
    eval, a = dsyevd(i)
    import LinearAlgebra
    ev2, a2 = LinearAlgebra.eigenvectors(i)
    x = _reconstruct(ev2, a2)
    assert _err(x - i) < 1e-08
    y = _reconstruct(eval, a)
    assert _err(y - i) < 1e-08
    assert _err(x - y) < 1e-08