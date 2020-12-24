# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.6/site-packages/PyLAF/lib.py
# Compiled at: 2010-07-26 23:16:21
from scipy import real, sqrt, rand, randn

def cvar(x):
    m = x.mean(-1)
    xo = (x.transpose() - m.transpose()).transpose()
    v = real(xo * xo.conj()).mean(-1)
    return (v, m)


def norm_mv(x):
    (v, m) = cvar(x)
    xn = ((x.transpose() - m.transpose()) / sqrt(v.transpose())).transpose()
    return (xn, m, v)


def crand(*arg):
    """
    complex uniform random n-d array
    """
    n = 1
    for i in arg:
        n = n * i

    if n < 100:
        o = 200
    else:
        o = 2 * n
    r = 2 * rand(o) - 1
    i = 2 * rand(o) - 1
    b = sqrt(r * r + i * i) < 1
    c = r[b.nonzero()][:n] + complex(0.0, 1.0) * i[b.nonzero()][:n]
    return c.reshape(*arg)


def crandn(*arg):
    return norm_mv(randn(*arg) + complex(0.0, 1.0) * randn(*arg))[0]