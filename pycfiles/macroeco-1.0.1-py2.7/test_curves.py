# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/macroeco/models/test_curves.py
# Compiled at: 2015-10-07 18:42:13
from __future__ import division
from numpy.testing import TestCase, assert_equal, assert_array_equal, assert_almost_equal, assert_array_almost_equal, assert_allclose, assert_, assert_raises
import numpy as np
from decimal import Decimal
from macroeco.models import *
import scipy as sp, scipy.stats as stats, matplotlib.pyplot as plt

class SAMPLING_SAR(TestCase):

    def test_reversible(self):
        S0, N0 = (20, 1000.0)
        As = np.array([100, 50, 10])
        Ns = N0 * As / As[0]
        Ss = sampling_sar.vals(As, S0, N0, sad_k=0.5, ssad_k=0.5, approx=True)
        for A, S, N in zip(As[1:], Ss[1:], Ns[1:]):
            assert_almost_equal(S0, sampling_sar.vals([A, As[0]], S, N, sad_k=0.5, ssad_k=0.5, approx=True)[1], decimal=5)


class SAMPLING_iterative_SAR(TestCase):

    def test_reversible(self):
        S0, N0 = (20, 1000.0)
        As = 1 / 2 ** np.arange(0, 4)
        Ns = N0 * As / As[0]
        Ss = sampling_sar_iterative.vals(As, S0, N0, sad_k=0.5, ssad_k=0.5, approx=True)
        assert_array_almost_equal(Ss[::-1], sampling_sar_iterative.vals(As[::-1], Ss[(-1)], Ns[(-1)], sad_k=0.5, ssad_k=0.5, approx=True), decimal=1)


class SAMPLING_EAR(TestCase):

    def test_no_upscale(self):
        assert_raises(NotImplementedError, sampling_ear.vals, [1, 2], 50, 1000, 1, 1)

    def test_make_green_plot(self):
        pass


class METE_SAR(TestCase):

    def test_reversible(self):
        S0, N0 = (100, 1000000.0)
        As = np.array([100, 50, 10])
        Ns = N0 * As / As[0]
        Ss = mete_sar.vals(As, S0, N0, approx=True)
        for A, S, N in zip(As[1:], Ss[1:], Ns[1:]):
            assert_almost_equal(S0, mete_sar.vals([A, As[0]], S, N, approx=True)[1], decimal=5)

    def test_reproduce_mcglinn_figure(self):
        pass

    def test_vals_up(self):
        pass


class METE_iterative_SAR(TestCase):

    def test_reversible(self):
        S0, N0 = (100, 1000000.0)
        As = 1 / 2 ** np.arange(0, 4)
        Ns = N0 * As / As[0]
        Ss = mete_sar_iterative.vals(As, S0, N0, approx=True)
        assert_array_almost_equal(Ss[::-1], mete_sar_iterative.vals(As[::-1], Ss[(-1)], Ns[(-1)], approx=True), decimal=1)

    def test_vals_down(self):
        pass

    def test_vals_up(self):
        S0, N0 = (86.6, 2015)
        As = [0.04, 0.08, 0.16, 0.32, 0.64, 1.28, 2.56]
        Ss = mete_sar_iterative.vals(As, S0, N0, approx=True)
        assert_array_almost_equal(Ss, [
         86.6, 106.0327113, 127.1223631, 149.7292838,
         173.7360065, 199.0452844, 225.5766732])


class METE_EAR(TestCase):

    def test_no_upscale(self):
        assert_raises(NotImplementedError, mete_ear.vals, [1, 2], 50, 1000)

    def test_mete_ear_with_data(self):
        BCI_S = 283
        BCI_N = 208310
        SERP_S = 28
        SERP_N = 60346
        areas_serp = 1 / 2 ** np.arange(0, 9) * 0.0016 * 10000
        serp_ear = mete_ear.vals(areas_serp, SERP_S, SERP_N, approx=True)
        areas_bci = 1 / 2 ** np.arange(0, 14) * 50 * 10000
        bci_ear = mete_ear.vals(areas_bci, BCI_S, BCI_N, approx=True)