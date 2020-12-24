# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\cgp\test\test_clampable.py
# Compiled at: 2013-01-14 06:47:43
__doc__ = 'Tests for `cgp.virtexp.elphys.clampable`.'
import numpy as np
from cgp.virtexp.elphys import clampable

def test_pairbcast():
    """Check that broadcasting works for long sequences of pairs."""
    pairs = [
     ((1, 2), 3)] + [(1, 1)] * 15 + [(4, (5, 6))]
    bc = clampable.pairbcast(*pairs)
    bc_ends = clampable.pairbcast(*(pairs[:1] + pairs[-1:]))
    for i, j in zip(bc, bc_ends):
        np.testing.assert_equal(i[:1] + i[-1:], j)

    for i in bc:
        for j in i[1:-1]:
            np.testing.assert_equal(j, (1, 1))