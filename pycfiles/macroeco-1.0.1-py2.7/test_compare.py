# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/macroeco/compare/test_compare.py
# Compiled at: 2015-10-07 18:42:13
from __future__ import division
from numpy.testing import TestCase, assert_equal, assert_array_equal, assert_almost_equal, assert_array_almost_equal, assert_allclose, assert_, assert_raises
from macroeco.compare import *
import numpy as np, scipy.stats as stats, macroeco.models as mod

class TestNLL(TestCase):

    def test_nll(self):
        R_res = 32.09469
        data = np.array([1, 2, 3, 4, 5])
        model = stats.norm(loc=0, scale=1)
        lglk = nll(data, model)
        assert_almost_equal(R_res, lglk, decimal=5)


class TestLRT(TestCase):

    def test_lrt_gives_right_answer(self):
        rand_samp = mod.nbinom_ztrunc.rvs(20, 0.5, size=100)
        mle_nbd = mod.nbinom_ztrunc.fit_mle(rand_samp)
        mle_logser = mod.logser.fit_mle(rand_samp)
        res = lrt(rand_samp, mod.nbinom_ztrunc(mu=mle_nbd[0], k_agg=mle_nbd[1]), mod.logser(p=mle_logser[0]))
        assert_equal(res[1] < 0.05, True)


class TestAIC(TestCase):

    def test_aic_basic(self):
        model = stats.norm(loc=0, scale=1)
        data = np.arange(1, 9)
        aic1 = AIC(data, model, corrected=False)
        expected = 222.703016531
        assert_almost_equal(aic1, expected, decimal=6)
        model = stats.gamma(a=2)
        data = [1, 1, 1, 2, 4, 5, 7, 12]
        aic1 = AIC(data, model, corrected=False)
        expected = 51.760607494
        assert_almost_equal(aic1, expected, decimal=6)
        model = stats.gamma(a=2, loc=0)
        aic1 = AIC(data, model, corrected=False)
        expected = 53.760607494
        assert_almost_equal(aic1, expected, decimal=6)

    def test_aic_given_params(self):
        model = stats.norm()
        data = np.arange(1, 9)
        aic1 = AIC(data, model, corrected=False, params=2)
        expected = 222.703016531
        assert_almost_equal(aic1, expected)
        model = stats.gamma(2)
        data = [1, 1, 1, 2, 4, 5, 7, 12]
        aic1 = AIC(data, model, corrected=False, params=1)
        expected = 51.760607494
        assert_almost_equal(aic1, expected, decimal=6)
        model = stats.gamma(2, 0)
        aic1 = AIC(data, model, corrected=False, params=2)
        expected = 53.760607494
        assert_almost_equal(aic1, expected, decimal=6)

    def test_aicc(self):
        model = stats.norm()
        data = np.arange(1, 9)
        aic1 = AIC(data, model, corrected=True, params=2)
        expected = 225.10302
        assert_almost_equal(expected, aic1, decimal=5)


class TestAICCompare(TestCase):

    def test_aic_delta_and_weights(self):
        data = [
         1, 1, 1, 2, 3, 4, 7, 23, 78]
        models = [stats.norm(scale=100), stats.norm(scale=99)]
        aic_vals = [ AIC(data, tm) for tm in models ]
        daic, aicw = AIC_compare(aic_vals)
        pred = np.array([0.47909787, 0.52090213])
        assert_array_almost_equal(aicw, pred)
        assert_array_almost_equal(daic, [daic[0] - daic[1], 0])


class TestRsquared(TestCase):

    def test_r_squared_repeated_data(self):
        test_data = np.random.randint(5, 100, 100)
        rsq = r_squared(test_data, test_data)
        rsq_one_one = r_squared(test_data, test_data, one_to_one=True)
        assert_equal(rsq, 1)
        assert_equal(rsq_one_one, 1)


class TestPrestonBin(TestCase):

    def test_bin_functionality(self):
        data = np.array([1, 1, 1, 1, 2, 2, 4, 4, 8, 16, 17.1, 89])
        vegan = np.array([4, 2, 2, 1, 1, 1, 0, 1], dtype=np.float)
        test_res = preston_bin(data, max(data))[0]
        assert_array_equal(test_res, vegan)
        data = np.array([1, 1, 1, 1, 4, 5, 6, 7, 12, 34, 56])
        vegan = np.array([4, 0, 1, 3, 1, 0, 2], dtype=np.float)
        test_res = preston_bin(data, max(data))[0]
        assert_array_equal(test_res, vegan)

    def test_bin_data_boundary(self):
        data = np.array([1, 2])
        vegan = np.array([1, 1], dtype=np.float)
        test_res = preston_bin(data, max(data))[0]
        assert_array_equal(test_res, vegan)
        data = np.array([1, 1, 1])
        vegan = np.array([3], dtype=np.float)
        test_res = preston_bin(data, max(data))[0]
        assert_array_equal(test_res, vegan)
        data = np.array([1, 2, 3])
        vegan = np.array([1, 1, 1], dtype=np.float)
        test_res = preston_bin(data, max(data))[0]
        assert_array_equal(test_res, vegan)