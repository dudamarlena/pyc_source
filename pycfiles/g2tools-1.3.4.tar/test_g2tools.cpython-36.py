# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gpl/software/python/g2tools/tests/test_g2tools.py
# Compiled at: 2018-06-24 15:46:57
# Size of source mod 2**32: 18525 bytes
"""
test_g2tools.py
"""
from __future__ import print_function
import unittest, numpy as np, gvar as gv
from g2tools import *
SHOW_OUTPUT = False

def optprint(*args):
    pass


if SHOW_OUTPUT:
    optprint = print
MPI = 0.13957
MK = 0.4937

class test_g2tools(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_moments(self):
        """ moments(G) """
        optprint('\n=========== Test moments')
        mom = moments([1.0, 2.0, 3.0, 2.0], nlist=[0, 2, 4])
        if not (mom[0] == 11.0 and mom[2] == 28.0 and mom[4] == 100.0):
            raise AssertionError
        else:
            mom = moments([1.0, 2.0, 3.0, 2.0], nlist=[0, 2, 4], tmax=1.0)
            assert mom[0] == 5.0 and mom[2] == 4.0 and mom[4] == 4.0
            mom = moments([1.0, 2.0, 3.0, 2.0], nlist=[0, 2, 4], tmin=1.1)
            assert mom[0] == 6.0 and mom[2] == 24.0 and mom[4] == 96.0
            mom = moments([1.0, 2.0, 3.0, 3.0, 2.0], nlist=[0, 2, 4])
            assert mom[0] == 11.0 and mom[2] == 28.0 and mom[4] == 100.0
            mom = moments([1.0, 2.0, 3.0, 2.0], nlist=[0, 2, 4], periodic=False)
            assert mom[0] == 15.0 and mom[2] == 64.0 and mom[4] == 424.0
            mom = moments([1.0, 2.0, 3.0, 2.0], nlist=[0, 2, 4], periodic=False, tmax=1.0)
            assert mom[0] == 5.0 and mom[2] == 4.0 and mom[4] == 4.0
            mom = moments([1.0, 2.0, 3.0, 2.0], nlist=[0, 2, 4], periodic=False, tmin=1.1)
            assert mom[0] == 10.0 and mom[2] == 60.0 and mom[4] == 420.0
            tayl = [1.0, -2.0, 3.0]
            mom = taylor2mom(tayl)
            assert mom[4] == 24.0 and mom[6] == 1440.0 and mom[8] == 120960.0
            assert numpy.allclose(mom2taylor(mom), tayl)
        optprint('nothing to report -- all is good')

    def test_moments_tmin_tmax(self):
        """ moments vs fourier """
        optprint('\n=========== moments vs fourier')
        N = 3
        ainv = 2.5
        Z = 1.5
        m = np.array([0.5, 1.0, 1.5])[:N, None]
        t = np.arange(100)[None, :]
        G = np.sum((m / 4 * np.exp(-t * m)), axis=0) / Z ** 2
        vpol = vacpol(moments(G, ainv=ainv, Z=Z, periodic=False))
        fvpol = fourier_vacpol(G, ainv=ainv, Z=Z, periodic=False)
        a_mu_m = a_mu(vpol, qmax=1000.0)
        a_mu_f = a_mu(fvpol, qmax=1000.0)
        self.assertLess(abs(1 - a_mu_m / a_mu_f), 0.0001)

    def test_pade_svd(self):
        """ pade_svd(tayl, n, m) """
        optprint('\n=========== Test pade_svd')
        e_exp = [
         1.0, 1.0, 0.5, 0.16666666666666666, 0.041666666666666664, 0.008333333333333333]
        p0, q0 = scipy_pade(e_exp, 2)
        p0 = p0.c[-1::-1]
        q0 = q0.c[-1::-1]
        p, q = pade_svd(e_exp, 3, 2)
        if not numpy.allclose(p, p0):
            raise AssertionError
        else:
            if not numpy.allclose(q, q0):
                raise AssertionError
            else:
                optprint('(3,2) Pade of exp(x) - num:', p)
                optprint('(3,2) Pade of exp(x) - den:', q)
                e = sum(p) / sum(q)
                optprint('Pade(x=1) = {:.6}    error = {:7.2}'.format(e, abs(e / numpy.exp(1) - 1.0)))
                p0, q0 = scipy_pade(e_exp[:4], 1)
                p0 = p0.c[::-1]
                q0 = q0.c[::-1]
                p, q = pade_svd(e_exp, 3, 2, rtol=0.1)
                assert numpy.allclose(p, p0)
                assert numpy.allclose(q, q0)
                optprint('(2,1) Pade of exp(x) - num:', p)
                optprint('(2,1) Pade of exp(x) - den:', q)
                e = sum(p) / sum(q)
                optprint('Pade(x=1) = {:.6}    error = {:7.2}'.format(e, abs(e / numpy.exp(1) - 1.0)))
                p, q = pade_svd(e_exp, 3, 2, rtol=0.9)
                optprint('(1,0) Pade of exp(x) - num:', p)
                optprint('(1,0) Pade of exp(x) - den:', q)
                e = sum(p) / sum(q)
                optprint('Pade(x=1) = {:.6}    error = {:7.2}'.format(e, abs(e / numpy.exp(1) - 1.0)))
                assert numpy.allclose(p, [1.0, 1.0])
            assert numpy.allclose(q, [1.0])

    def test_pade_svd_consistency(self):
        """ pade_svd self consistency """
        x = gv.powerseries.PowerSeries([0, 1], order=20)
        f = np.exp(x).c
        m, n = (7, 7)
        for rtol in (1, 0.1, 0.01, 0.001):
            a, b = pade_svd(f, m, n, rtol=rtol)
            mm = len(a) - 1
            nn = len(b) - 1
            if (m, n) != (mm, nn):
                aa, bb = pade_svd(f, mm, nn)
                self.assertTrue(np.allclose(aa, a))
                self.assertTrue(np.allclose(bb, b))

    def test_pade_gvar(self):
        """ pade_gvar(tayl, m, n) """
        optprint('\n=========== Test pade_gvar')
        e_exp = [1.0, 1.0, 0.5, 0.16666666666666666, 0.041666666666666664, 0.008333333333333333, 0.001388888888888889]

        def _scipy_pade(m, n):
            p, q = scipy_pade(e_exp[:m + n + 1], n)
            return (p.c[-1::-1], q.c[-1::-1])

        def print_result(p, q):
            optprint('num =', p)
            optprint('den =', q)

        def test_result(p, q, e_exp):
            m = len(p) - 1
            n = len(q) - 1
            p0, q0 = _scipy_pade(m, n)
            try:
                assert numpy.allclose(gvar.mean(p), p0)
            except:
                print(m, n, p0, p, q0, q)

            if not numpy.allclose(gvar.mean(q), q0):
                raise AssertionError
            else:
                num = gvar.powerseries.PowerSeries(p, order=(m + n))
                den = gvar.powerseries.PowerSeries(q, order=(m + n))
                ratio = (num / den).c / e_exp[:m + n + 1]
                assert numpy.allclose(gvar.mean(ratio), 1.0)
                assert numpy.allclose(gvar.sdev(ratio), 0.0)

        e_exp_noise = [x * gvar.gvar('1.0(1)') for x in e_exp]
        p, q = pade_gvar(e_exp_noise, 3, 2)
        print_result(p, q)
        self.assertEqual(len(p), 3)
        self.assertEqual(len(q), 2)
        test_result(p, q, e_exp_noise)
        e_exp_noise = [x * gvar.gvar('1.0(3)') for x in e_exp]
        p, q = pade_gvar(e_exp_noise, 3, 2)
        self.assertEqual(len(p), 2)
        self.assertEqual(len(q), 2)
        test_result(p, q, e_exp_noise)

    def test_amu(self):
        """ a_mu(vpol) """
        optprint('\n=========== Test a_mu')

        def no_vacpol(q2):
            return 0.25 / ALPHA ** 2

        amu = a_mu(no_vacpol)
        optprint('coef of alpha/pi = {}   error = {:7.2}'.format(amu, abs(amu - 0.5) / 0.5))
        if not numpy.allclose(amu, 0.5):
            raise AssertionError
        else:
            amu = a_mu(vacpol.fermion(m=Mmu))
            exact = (ALPHA / numpy.pi) ** 2 * (3.3055555555555554 - numpy.pi ** 2 / 3.0)
            optprint('a_mu(m=mu) = {}    error = {:7.2}'.format(amu, abs(amu / exact - 1.0)))
            assert numpy.allclose(amu / exact, 1.0)
            ratio = 100000.0
            amu = a_mu(vacpol.fermion(Mmu / ratio))
            exact = (ALPHA / numpy.pi) ** 2 * (numpy.log(ratio) / 3.0 - 0.6944444444444444)
            assert numpy.allclose((amu / exact), 1.0, rtol=(3 / ratio))

    def test_noise(self):
        """ a_mu(vpol) with noisy fermion loop """
        optprint('\n=========== Test noise (fermion loop)')

        def print_result(tag, amu, exact, pihat):
            line = '{:11} {:<13} {:15} {:15} {:15}'
            line = line.format(tag, amu if isinstance(amu, gvar.GVar) else '{:.8}'.format(amu), '  error = {:7.2}'.format(abs(gvar.mean(amu) / exact - 1.0)), '  order = {}'.format(pihat.order), '  bad poles = {}'.format(pihat.badpoles()))
            optprint(line)

        pihat_exact = vacpol.fermion(m=0.4937)
        exact = a_mu(pihat_exact)
        pihat = vacpol(pihat_exact.taylor(), (9, 9))
        amu = a_mu(pihat)
        print_result('1loop(mK):', amu, exact, pihat)
        if not numpy.allclose((amu / exact), 1.0, rtol=1e-05):
            raise AssertionError
        else:
            tayl = [ci * gvar.gvar('1.00(1)') for ci in pihat_exact.taylor()]
            pihat = vacpol(tayl, (2, 2))
            amu = a_mu(pihat)
            print_result('1loop(mK):', amu, exact, pihat)
            assert numpy.allclose((amu.mean / exact), 1.0, rtol=0.01)
            pihat_exact = vacpol.fermion(m=MPI)
            exact = a_mu(pihat_exact)
            pihat = vacpol(pihat_exact.taylor(), (9, 9))
            amu = a_mu(pihat)
            print_result('1loop(mpi):', amu, exact, pihat)
            assert numpy.allclose((amu / exact), 1.0, rtol=0.0001)
            tayl = [ci * gvar.gvar('1.00(1)') for ci in pihat_exact.taylor()]
            pihat = vacpol(tayl, (2, 2), warn=True)
            amu = a_mu(pihat)
            print_result('1loop(mpi):', amu, exact, pihat)
            assert numpy.allclose((amu.mean / exact), 1.0, rtol=0.01)

    def test_scalar(self):
        """ vacpole.scalar(mpi) """
        optprint('\n=========== Test scalar loop')
        for mpi, amu_vegas in [(MPI, '7.076903(1)e-9'), (MK, '6.631148(1)e-10')]:
            amu = a_mu(vacpol.scalar(mpi))
            amu_vegas = gvar.gvar(amu_vegas)
            diff = gvar.fabs(amu - amu_vegas)
            assert diff.mean < 5 * diff.sdev
            optprint('1-loop({}) = {!s}   error = {}'.format(mpi, amu, diff))

    def test_exact_vs_pade(self):
        """ a_mu from pade vs from function"""
        optprint('\n=========== Test exact vs pade')
        m = MPI
        for n in (4, 5, 6, 7):
            for f in [('scalar', vacpol.scalar),
             (
              'fermion', vacpol.fermion),
             (
              'vector', vacpol.vector)]:
                amu_exact = a_mu(f[1](m, n=n))
                vpol = f[1](m, n=n, use_pade=True)
                amu_pade = a_mu(vpol)
                optprint('{:>7}:  order = {}   pade/exact = {}'.format(f[0], vpol.order, amu_pade / amu_exact))
                assert abs(amu_pade / amu_exact - 1.0) < 0.01

            optprint('-----')

    def test_exact_vs_fourier(self):
        """ a_mu from pade vs from function"""
        optprint('\n=========== Test exact vs fourier')
        N = 3
        ainv = 2.5
        Z = 1.5
        m = np.array([0.5, 1.0, 1.5])[:N, None]
        t = np.arange(100)[None, :]
        G = np.sum((m / 4 * np.exp(-t * m)), axis=0) / Z ** 2
        fvpol = fourier_vacpol(G, ainv=ainv, Z=Z, periodic=False)
        a_mu_fourier = a_mu(fvpol, qmax=1000.0)
        optprint('a_mu from fourier: {}'.format(a_mu_fourier))
        for n in range(1, N + 1):
            a_mu_exact = np.sum([a_mu(vacpol.vector(mi * ainv)) * ainv ** 2 for mi in m[:n]])
            optprint('a_mu from {} states: {}'.format(n, a_mu_exact))

        self.assertLess(abs(1 - a_mu_fourier / a_mu_exact), 0.0001)

    def test_fourier_tmin_tmax(self):
        """  fourier_vacpol with tmin,tmax """
        optprint('\n=========== Test exact vs fourier')
        N = 3
        ainv = 2.5
        Z = 1.5
        m = np.array([0.5, 1.0, 1.5])[:N, None]
        t = np.arange(100)[None, :]
        G = np.sum((m / 4 * np.exp(-t * m)), axis=0) / Z ** 2
        fvpol = fourier_vacpol(G, ainv=ainv, Z=Z, periodic=False)
        fvpolp = fourier_vacpol(G, ainv=ainv, Z=Z, periodic=False, tmin=10.0)
        fvpolm = fourier_vacpol(G, ainv=ainv, Z=Z, periodic=False, tmax=10.0)
        a_mu_all = a_mu(fvpol, qmax=1000.0)
        a_mu_p = a_mu(fvpolp, qmax=1000.0)
        a_mu_m = a_mu(fvpolm, qmax=1000.0)
        self.assertLess(abs(1 - a_mu_all / (a_mu_p + a_mu_m)), 1e-06)

    def test_exact_vs_fourier_periodic(self):
        """ a_mu from pade vs from function"""
        optprint('\n=========== Test exact vs fourier')
        for start in (-2, -1):
            N = 3
            ainv = 2.5
            Z = 1.5
            m = np.array([0.5, 1.0, 1.5])[:N, None]
            t = np.arange(100)
            t = np.concatenate((t, t[start:0:-1]))
            G = np.sum((m / 4 * np.exp(-t * m)), axis=0) / Z ** 2
            fvpol = fourier_vacpol(G, ainv=ainv, Z=Z, periodic=True)
            a_mu_fourier = a_mu(fvpol, qmax=1000.0)
            optprint('a_mu from fourier: {}'.format(a_mu_fourier))
            for n in range(1, N + 1):
                a_mu_exact = np.sum([a_mu(vacpol.vector(mi * ainv)) * ainv ** 2 for mi in m[:n]])
                optprint('a_mu from {} states: {}'.format(n, a_mu_exact))

            self.assertLess(abs(1 - a_mu_fourier / a_mu_exact), 0.0001)

    def test_fourier_periodic_tmin_tmax(self):
        """ a_mu from pade vs from function"""
        optprint('\n=========== Test exact vs fourier')
        for start in (-2, -1):
            N = 3
            ainv = 2.5
            Z = 1.5
            m = np.array([0.5, 1.0, 1.5])[:N, None]
            t = np.arange(100)
            t = np.concatenate((t, t[start:0:-1]))
            G = np.sum((m / 4 * np.exp(-t * m)), axis=0) / Z ** 2
            fvpol = fourier_vacpol(G, ainv=ainv, Z=Z, periodic=True)
            fvpolp = fourier_vacpol(G, ainv=ainv, Z=Z, periodic=True, tmin=10.0)
            fvpolm = fourier_vacpol(G, ainv=ainv, Z=Z, periodic=True, tmax=10.0)
            a_mu_all = a_mu(fvpol, qmax=1000.0)
            a_mu_p = a_mu(fvpolp, qmax=1000.0)
            a_mu_m = a_mu(fvpolm, qmax=1000.0)
            self.assertLess(abs(1 - a_mu_all / (a_mu_p + a_mu_m)), 1e-06)

    def test_exact_vs_vacpol_FT(self):
        """ a_mu from fourier_vacpol(vacpol.FT) """
        optprint('\n=========== Test exact vs fourier')
        N = 3
        ainv = 2.5
        Z = 1.5
        m = np.array([0.5, 1.0, 1.5])[:N, None]
        t = np.arange(100)[None, :]
        G = np.sum((m / 4 * np.exp(-t * m)), axis=0) / Z ** 2
        t = t.reshape(-1)
        m = m.reshape(-1)
        vpol = vacpol(moments(G, ainv=ainv, Z=Z, periodic=False), order=(3, 3))
        self.assertLess(np.fabs(vpol.E[(-1)] - m[0] * ainv) / m[0] * ainv, 1e-06)
        self.assertLess(np.fabs(vpol.ampl[(-1)] - m[0] * ainv ** 3 / 4) / (m[0] * ainv ** 3 / 4), 1e-06)
        fvpol = fourier_vacpol(vpol.FT(t, ainv=ainv), ainv=ainv, periodic=False)
        a_mu_fmom = a_mu(fvpol, qmax=1000.0)
        optprint('a_mu from FT of moments: {}'.format(a_mu_fmom))
        for n in range(1, N + 1):
            a_mu_exact = np.sum([a_mu(vacpol.vector(mi * ainv)) * ainv ** 2 for mi in m[:n]])
            optprint('a_mu from {} states: {}'.format(n, a_mu_exact))

        self.assertLess(abs(1 - a_mu_fmom / a_mu_exact), 0.0001)

    def test_vacpol_poles(self):
        """ vacpol.poles and vacpol.residues """
        m1 = gv.gvar('1.0(1)')
        f1 = gv.gvar('0.25(1)')
        vpol1 = vacpol.vector(m1, f=f1)
        m2 = gv.gvar('2.0(1)')
        f2 = gv.gvar('0.5(1)')
        vpol2 = vacpol.vector(m2, f=f2)
        vpol = vacpol((vpol1.taylor() + vpol2.taylor()), order=(2, 2))
        self.assertEqual(gv.fabs(vpol.poles[0] + m2 ** 2).fmt(5), '0.00000(0)')
        self.assertEqual(gv.fabs(vpol.residues[0] + f2 ** 2 / 2).fmt(5), '0.00000(0)')
        self.assertEqual(gv.fabs(vpol.poles[1] + m1 ** 2).fmt(5), '0.00000(0)')
        self.assertEqual(gv.fabs(vpol.residues[1] + f1 ** 2 / 2).fmt(5), '0.00000(0)')

    def test_warn_exception(self):
        """ vacpol(warn=True) """
        tayl = np.array([0.0108361463, -0.0397340348, 0.226639708,
         -1.58653778, 12.5300529, -107.205606,
         971.19329, -9184.08638, 89803.3421,
         -901971.926])
        tayl = tayl * gv.gvar(len(tayl) * ['1(1)'])
        tayl += np.array([5.12534367e-05, -0.000270757996, 0.000549464167,
         -0.0269828134, 0.0943691955, -1.64530731,
         0.0497938388, -11.0418131, -724.696697,
         25903.0047])
        with self.assertRaises(ValueError):
            vpol = vacpol(tayl, warn=True, qth=(2 * MPI), order=(3, 3), rtol=1e-14)
        with warnings.catch_warnings(record=True) as (w):
            warnings.simplefilter('always')
            m = gv.gvar('1.0(1)')
            f = gv.gvar('0.25(1)')
            vpol = vacpol((vacpol.vector(m, f, n=10).taylor()), order=(3, 3), warn=True)
            self.assertTrue(w)
            self.assertEqual(vpol.order, (1, 1))


if __name__ == '__main__':
    unittest.main()