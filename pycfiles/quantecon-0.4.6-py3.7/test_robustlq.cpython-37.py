# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quantecon/tests/test_robustlq.py
# Compiled at: 2019-11-04 18:33:25
# Size of source mod 2**32: 3452 bytes
"""
Tests for robustlq.py

"""
import sys, unittest, numpy as np
from numpy.testing import assert_allclose
from quantecon.lqcontrol import LQ
from quantecon.robustlq import RBLQ

class TestRBLQControl(unittest.TestCase):

    def setUp(self):
        a_0 = 100
        a_1 = 0.5
        rho = 0.9
        sigma_d = 0.05
        beta = 0.95
        c = 2
        gamma = 50.0
        theta = 0.002
        ac = (a_0 - c) / 2.0
        R = np.array([[0, ac, 0],
         [
          ac, -a_1, 0.5],
         [
          0.0, 0.5, 0]])
        R = -R
        Q = gamma / 2
        Q_pf = 0.0
        A = np.array([[1.0, 0.0, 0.0],
         [
          0.0, 1.0, 0.0],
         [
          0.0, 0.0, rho]])
        B = np.array([[0.0],
         [
          1.0],
         [
          0.0]])
        B_pf = np.zeros((3, 1))
        C = np.array([[0.0],
         [
          0.0],
         [
          sigma_d]])
        self.rblq_test = RBLQ(Q, R, A, B, C, beta, theta)
        self.rblq_test_pf = RBLQ(Q_pf, R, A, B_pf, C, beta, theta)
        self.lq_test = LQ(Q, R, A, B, C, beta=beta)
        self.methods = ['doubling', 'qz']

    def tearDown(self):
        del self.rblq_test
        del self.rblq_test_pf

    def test_pure_forecasting(self):
        self.assertTrue(self.rblq_test_pf.pure_forecasting)

    def test_robust_rule_vs_simple(self):
        rblq = self.rblq_test
        rblq_pf = self.rblq_test_pf
        for method in self.methods:
            Fr, Kr, Pr = self.rblq_test.robust_rule(method=method)
            Fr_pf, Kr_pf, Pr_pf = self.rblq_test_pf.robust_rule(method=method)
            Fs, Ks, Ps = rblq.robust_rule_simple(P_init=Pr, tol=1e-12)
            Fs_pf, Ks_pf, Ps_pf = rblq_pf.robust_rule_simple(P_init=Pr_pf,
              tol=1e-12)
            assert_allclose(Fr, Fs, rtol=0.0001)
            assert_allclose(Kr, Ks, rtol=0.0001)
            assert_allclose(Pr, Ps, rtol=0.0001)
            atol = 1e-10
            assert_allclose(Fr_pf, Fs_pf, rtol=0.0001)
            assert_allclose(Kr_pf, Ks_pf, rtol=0.0001, atol=atol)
            assert_allclose(Pr_pf, Ps_pf, rtol=0.0001, atol=atol)

    def test_f2k_and_k2f(self):
        rblq = self.rblq_test
        for method in self.methods:
            Fr, Kr, Pr = self.rblq_test.robust_rule(method=method)
            K_f2k, P_f2k = rblq.F_to_K(Fr, method=method)
            F_k2f, P_k2f = rblq.K_to_F(Kr, method=method)
            assert_allclose(K_f2k, Kr, rtol=0.0001)
            assert_allclose(F_k2f, Fr, rtol=0.0001)
            assert_allclose(P_f2k, P_k2f, rtol=0.0001)

    def test_evaluate_F(self):
        rblq = self.rblq_test
        for method in self.methods:
            Fr, Kr, Pr = self.rblq_test.robust_rule(method=method)
            Kf, Pf, df, Of, of = rblq.evaluate_F(Fr)
            assert_allclose(Pf, Pr)
            assert_allclose(Kf, Kr)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRBLQControl)
    unittest.TextTestRunner(verbosity=2, stream=(sys.stderr)).run(suite)