# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/plugins/Linear_prediction.py
# Compiled at: 2018-03-06 06:50:33
# Size of source mod 2**32: 2667 bytes
"""plugin for the Linear Prediction algos into NPKDATA

"""
from __future__ import print_function
import unittest
from spike import NPKError
from spike.NPKData import NPKData_plugin
from spike.Algo.Linpredic import burgr, burgc, predict

def lpext2d(npkd, final_size, lprank=10, algotype='burg'):
    """
    extends a 2D FID in F1 up to final_size, using lprank coefficients, and algotype mode
    """
    npkd.check2D()
    init_size = npkd.size1
    if lprank > init_size / 2 or lprank < 2:
        NPKError('error with lprank', data=npkd)
    elif algotype == 'burg':
        if npkd.axis1.itype == 1:
            method = burgc
        else:
            method = burgr
    else:
        raise Exception('Only burg algorithm implemented in lpext for the moment')
    k = npkd.axis1.itype + 1
    npkd.chsize(sz1=(k * final_size))
    for i, r in enumerate(npkd.xcol()):
        buf = r.get_buffer()[0:init_size]
        coeffs = method(lprank, buf)
        predicted = predict(buf, coeffs, final_size)
        r.set_buffer(predicted)
        npkd.set_col(i, r)

    return npkd


def lpext1d(npkd, final_size, lprank=10, algotype='burg'):
    """
    extends the current FID up to final_size, using lprank coefficients, and algotype mode
    """
    npkd.check1D()
    if lprank > npkd.size1 / 2 or lprank < 2:
        NPKError('error with lprank', data=npkd)
    elif algotype == 'burg':
        if npkd.axis1.itype == 1:
            method = burgc
        else:
            method = burgr
    else:
        raise Exception('Only burg algorithm implemented in lpext for the moment')
    coeffs = method(lprank, npkd.get_buffer())
    predicted = predict(npkd.buffer, coeffs, final_size)
    npkd.set_buffer(predicted)
    npkd.adapt_size()
    return npkd


def lpext(npkd, final_size, lprank=10, algotype='burg'):
    """
    extends a 1D FID or 2D FID in F1 up to final_size, using lprank coefficients, and algotype mode
    """
    if npkd.dim == 1:
        return lpext1d(npkd, final_size, lprank=10, algotype='burg')
    if npkd.dim == 2:
        return lpext2d(npkd, final_size, lprank=10, algotype='burg')
    raise Exception('Not implemented yet')


class LinpredicTests(unittest.TestCase):

    def setUp(self):
        self.verbose = 1

    def announce(self):
        if self.verbose > 0:
            print(self.shortDescription())

    def test_log(self):
        """testing log"""
        import math
        self.announce()
        x = 0.0
        y = math.log(1.0)
        self.assertAlmostEqual(x, y)


NPKData_plugin('lpext', lpext)