# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/colibri/perturbation_theory.py
# Compiled at: 2020-04-14 11:56:34
import colibri.constants as const, numpy as np, colibri.cosmology as cc, scipy.special as ss, scipy.integrate as integrate, scipy.interpolate as si, colibri.useful_functions as UF, itertools
from six.moves import xrange

class spt:
    """
        The 'spt' class contains routines relative to cosmological Standard Perturbation Theory such as
        vertices and kernels. Currently it contains routines to compute the 1-loop matter power spectrum
        ad the tree-level bispectrum.
        The instance to call it takes the following arguments.

        Parameters
        ----------

        'z': array, default = 0
            Redshifts.

        'k_p': array, default = np.logspace(-4., 1., 31)
            Scales for P(k) in h/Mpc.

        'k_b': array, default = np.logspace(-4., 1., 31)
            Scales for bispectrum in h/Mpc.

        'code': what, default = 'camb'
            Boltzmann solver to compute linear power spectrum: choose between 'camb', 'class'.

        'fundamental': what, default = 'cb'
            Density field to use: choose between 'cb', 'tot' for CDM+baryons and total matter respectively.

        'cosmology': 'cosmo' instance, default = see 'cosmology.py'
            A 'cosmo' instance containing cosmological parameters.

        When called, the class immediately loads the linear power spectrum according to 'code' and  'fundamental'. This quantities are stored in 'k_load' and 'pk_load'. Also the linear power spectrum at 'k_p' is returned ('Pk_L') and an interpolation of it at all scales ('power_l_q')

        'k_load': array
            Array of scales in h/Mpc, np.logspace(-4,2.5,501).

        'pk_load': 2D array
            Power spectrum evaluated at ('z', 'k_load').

        'Pk': dictionary
            Only one key is initialized, Pk['1-1'], with the linear power spectrum evaluated at 'z', 'k_p'.

        'power_l_q': interpolated object
            interpolation for P(k,z).

        """

    def __init__(self, z=0.0, k_p=np.logspace(-4.0, -1.0, 31), k_b=np.logspace(-4.0, -1.0, 31), code='camb', fundamental='cb', cosmology=cc.cosmo()):
        self.z = z
        self.k_p = k_p
        self.k_b = k_b
        self.n_k_p = len(self.k_p)
        self.n_k_b = len(self.k_b)
        self.cosmology = cosmology
        self.fundamental = fundamental
        self.code = code
        NPOINTS = 501
        LOGKMIN = -4.05
        LOGKMAX = 2.55
        if code == 'camb':
            self.k_load, self.pk_load = self.cosmology.camb_Pk(z=self.z, k=np.logspace(LOGKMIN, LOGKMAX, NPOINTS), nonlinear=False, var_1=self.fundamental, var_2=self.fundamental)
            self.pk_load = self.pk_load / (2.0 * np.pi) ** 3.0
        else:
            self.k_load, self.pk_load = self.cosmology.class_XPk(z=self.z, k=np.logspace(LOGKMIN, LOGKMAX, NPOINTS), nonlinear=False, var_1=[
             self.fundamental], var_2=[
             self.fundamental])
            self.pk_load = self.pk_load[(0, 0)] / (2.0 * np.pi) ** 3.0
        self.Pk = {}
        self.nz = np.size(self.z)
        if self.nz == 1:
            power_linear = si.interp1d(self.k_load, self.pk_load[0], kind='cubic')
            self.Pk['lin'] = np.array([power_linear(self.k_p)])
            self.Pk['1-1'] = self.Pk['lin']
            k_q, Pk_q = UF.extrapolate_log(self.k_load, self.pk_load[0], 1e-08, 100000000.0)
            self.power_l_q = si.interp1d(k_q, Pk_q, kind='linear')
        else:
            power_linear = si.interp2d(self.k_load, self.z, self.pk_load, kind='linear')
            self.Pk['lin'] = power_linear(self.k_p, self.z)
            Pk_q = []
            for i in range(self.nz):
                k_q, P_tmp = UF.extrapolate_log(self.k_load, self.pk_load[i], 1e-08, 100000000.0)
                Pk_q.append(P_tmp)

            Pk_q = np.array(Pk_q)
            self.power_l_q = si.interp2d(k_q, self.z, Pk_q, kind='linear')

    def alpha(self, k_1, k_2):
        """
                Vertex in SPT given two 3-vectors.

                Parameters
                ----------

                'k_1': array of size 3
                    First 3-vector.

                'k_2': array of size 3
                    Second 3-vector.

                Returns
                ----------

                float
                """
        k_1 += np.finfo(float).eps
        k_2 += np.finfo(float).eps
        K = np.sum((k_1, k_2), axis=0)
        k_1_m = np.linalg.norm(k_1)
        k_2_m = np.linalg.norm(k_2)
        K_m = np.linalg.norm(K)
        return np.dot(K, k_1) / k_1_m ** 2.0

    def beta(self, k_1, k_2):
        """
                Vertex in SPT given two 3-vectors.

                Parameters
                ----------

                'k_1': array of size 3
                    First 3-vector.

                'k_2': array of size 3
                    Second 3-vector.

                Returns
                ----------

                float
                """
        k_1 += np.finfo(float).eps
        k_2 += np.finfo(float).eps
        K = np.sum((k_1, k_2), axis=0)
        k_1_m = np.linalg.norm(k_1)
        k_2_m = np.linalg.norm(k_2)
        K_m = np.linalg.norm(K)
        return np.dot(k_1, k_2) * K_m ** 2.0 / (2.0 * k_1_m ** 2.0 * k_2_m ** 2.0)

    def F(self, n, kk=[]):
        """
                F kernel of any order, given a set of 3-vectors. The number of vectors
        must match the order of the kernel.
        N.B. This kernel is not symmetrized!

                Parameters
                ----------

                'n': int
                    Kernel order.

                'kk': list, default  = []
                    List of 3-vectors at which to compute the kernel.

                Returns
                ----------

                float
                """
        if n != len(kk):
            raise ValueError('Error! Number of arguments must match order of kernel')
        else:
            for i in range(len(kk)):
                kk = np.array(kk) + np.finfo(float).eps

        if n == 1.0:
            return 1.0
        else:
            factor = 1.0 / ((2.0 * n + 3.0) * (n - 1.0))
            result = 0.0
            for m in range(1, n):
                arg_1st = kk[:m]
                arg_2nd = kk[m:n]
                K1 = np.sum(arg_1st, axis=0)
                K2 = np.sum(arg_2nd, axis=0)
                alp = self.alpha(K1, K2)
                bet = self.beta(K1, K2)
                result += factor * self.G(m, kk=arg_1st) * ((2.0 * n + 1.0) * alp * self.F(n - m, arg_2nd) + 2.0 * bet * self.G(n - m, arg_2nd))

            return result

    def F_symm(self, n, kk=[]):
        """
                Symmetrized F kernel of any order, given a set of 3-vectors. The number of vectors
        must match the order of the kernel.

                Parameters
                ----------

                'n': int
                    Kernel order.

                'kk': list, default  = []
                    List of 3-vectors at which to compute the kernel.

                Returns
                ----------

                float
                """
        comb = np.math.factorial(n)
        perm = np.array(list(itertools.permutations(kk))).tolist()
        tot = 0.0
        for p in perm:
            tot += self.F(n, p)

        return tot / comb

    def G(self, n, kk):
        """
                G kernel of any order, given a set of 3-vectors. The number of vectors
        must match the order of the kernel.
        N.B. This kernel is not symmetrized!

                Parameters
                ----------

                'n': int
                    Kernel order.

                'kk': list, default  = []
                    List of 3-vectors at which to compute the kernel.

                Returns
                ----------

                float
                """
        if n != len(kk):
            raise ValueError('Error! Number of arguments must match order of kernel')
        else:
            kk = np.array(kk) + np.finfo(float).eps
        if n == 1.0:
            return 1.0
        else:
            factor = 1.0 / ((2.0 * n + 3.0) * (n - 1.0))
            result = 0.0
            for m in range(1, n):
                arg_1st = kk[:m]
                arg_2nd = kk[m:n]
                K1 = np.sum(arg_1st, axis=0)
                K2 = np.sum(arg_2nd, axis=0)
                alp = self.alpha(K1, K2)
                bet = self.beta(K1, K2)
                result += factor * self.G(m, kk=arg_1st) * (3.0 * alp * self.F(n - m, arg_2nd) + 2.0 * n * bet * self.G(n - m, arg_2nd))

            return result

    def G_symm(self, n, kk=[]):
        """
                Symmetrized G kernel of any order, given a set of 3-vectors. The number of vectors
        must match the order of the kernel.

                Parameters
                ----------

                'n': int
                    Kernel order.

                'kk': list, default  = []
                    List of 3-vectors at which to compute the kernel.

                Returns
                ----------

                float
                """
        comb = np.math.factorial(n)
        perm = np.array(list(itertools.permutations(kk))).tolist()
        tot = 0.0
        for p in perm:
            tot += self.G(n, p)

        return tot / comb

    def F_2_brute(self, k1, k2, mu):
        """
                Brute formula for the symmetrized 'F_2' kernel given the amplitude of the two
                vectors and the cosine of the angle between them.

                Parameters
                ----------

                'k1': float
                    Length of first vector.

                'k2': float
                    Length of second vector.

                'mu': float
                    cosine of the angle between k1 and k2.

                Returns
                ----------

                float
                """
        return 5.0 / 7.0 + 1.0 / 2.0 * mu * (k1 / k2 + k2 / k1) + 2.0 / 7.0 * mu ** 2.0

    def G_2_brute(self, k1, k2, mu):
        """
                Brute formula for the symmetrized 'G_2' kernel given the amplitude of the two
                vectors and the cosine of the angle between them.

                Parameters
                ----------

                'k1': float
                    Length of first vector.

                'k2': float
                    Length of second vector.

                'mu': float
                    cosine of the angle between k1 and k2.

                Returns
                ----------

                float
                """
        return 3.0 / 7.0 + 1.0 / 2.0 * mu * (k1 / k2 + k2 / k1) + 4.0 / 7.0 * mu ** 2.0

    def F_2(self, k1, k2, mu):
        """
                Symmetrized 'F_2' kernel given the amplitude of the two vectors and the cosine of the angle
                between them.

                Parameters
                ----------

                'k1': float
                    Length of first vector.

                'k2': float
                    Length of second vector.

                'mu': float
                    cosine of the angle between k1 and k2.

                Returns
                ----------

                float
                """
        k1_vec = np.array([0.0, 0.0, 1.0]) * k1
        k2_vec = np.array([np.sqrt(1.0 - mu ** 2.0), 0.0, mu]) * k2
        return self.F_symm(2, kk=[k1_vec, k2_vec])

    def G_2(self, k1, k2, mu):
        """
                Symmetrized 'G_2' kernel given the amplitude of the two vectors and the cosine of the angle
                between them.

                Parameters
                ----------

                'k1': float
                    Length of first vector.

                'k2': float
                    Length of second vector.

                'mu': float
                    cosine of the angle between k1 and k2.

                Returns
                ----------

                float
                """
        k1_vec = np.array([0.0, 0.0, 1.0]) * k1
        k2_vec = np.array([np.sqrt(1.0 - mu ** 2.0), 0.0, mu]) * k2
        return self.G_symm(2, kk=[k1_vec, k2_vec])

    def F_3(self, k1, k2, k3, mu12, mu23, mu13):
        """
                Symmetrized 'F_3' kernel given the amplitude of the two vectors and the cosine of the angles
                among them.

                Parameters
                ----------

                'k1': float
                    Length of first vector.

                'k2': float
                    Length of second vector.

                'k3': float
                    Length of third vector.

                'mu12': float
                    cosine of the angle between k1 and k2.

                'mu23': float
                    cosine of the angle between k2 and k3.

                'mu13': float
                    cosine of the angle between k1 and k3.

                Returns
                ----------

                float
                """
        mu12 -= np.finfo(float).eps * np.sign(mu12)
        mu23 -= np.finfo(float).eps * np.sign(mu23)
        mu13 -= np.finfo(float).eps * np.sign(mu13)
        sin_theta_12 = (1.0 - mu12 ** 2.0) ** 0.5
        sin_theta_13 = (1.0 - mu13 ** 2.0) ** 0.5
        sin_phi_13 = (mu23 - mu12 * mu13) / (sin_theta_12 * sin_theta_13)
        cos_phi_13 = (1.0 - sin_phi_13 ** 2.0) ** 0.5
        k1_vec = np.array([0.0, 0.0, 1.0]) * k1
        k2_vec = np.array([sin_theta_12, 0.0, mu12]) * k2
        k3_vec = np.array([sin_phi_13 * sin_theta_13, cos_phi_13 * sin_theta_13, mu13]) * k3
        return self.F_symm(3, kk=[k1_vec, k2_vec, k3_vec])

    def G_3(self, k1, k2, k3, mu12, mu23, mu13):
        """
                Symmetrized 'G_3' kernel given the amplitude of the two vectors and the cosine of the angles
                among them.

                Parameters
                ----------

                'k1': float
                    Length of first vector.

                'k2': float
                    Length of second vector.

                'k3': float
                    Length of third vector.

                'mu12': float
                    cosine of the angle between k1 and k2.

                'mu23': float
                    cosine of the angle between k2 and k3.

                'mu13': float
                    cosine of the angle between k1 and k3.

                Returns
                ----------

                float
                """
        mu12 -= np.finfo(float).eps * np.sign(mu12)
        mu23 -= np.finfo(float).eps * np.sign(mu23)
        mu13 -= np.finfo(float).eps * np.sign(mu13)
        sin_theta_12 = (1.0 - mu12 ** 2.0) ** 0.5
        sin_theta_13 = (1.0 - mu13 ** 2.0) ** 0.5
        sin_phi_13 = (mu23 - mu12 * mu13) / (sin_theta_12 * sin_theta_13)
        cos_phi_13 = (1.0 - sin_phi_13 ** 2.0) ** 0.5
        k1_vec = np.array([0.0, 0.0, 1.0]) * k1
        k2_vec = np.array([sin_theta_12, 0.0, mu12]) * k2
        k3_vec = np.array([sin_phi_13 * sin_theta_13, cos_phi_13 * sin_theta_13, mu13]) * k3
        return self.G_symm(3, kk=[k1_vec, k2_vec, k3_vec])

    def Pk_1_loop(self):
        """
                1-loop power spectrum in SPT, i.e the sum P_22 and P_13.

                Returns
                ----------

                Nothing, but adds self.Pk['2-2'], self.Pk['1-3'] and Pk['1 loop'] to the self.Pk dictionary
                """
        kL = self.k_load
        PL = self.pk_load
        kkL, kL2, kL3, kL4, kL5, kL6, kL7, kL8 = (
         2 * kL, kL * kL, kL * kL * kL, kL * kL * kL * kL, kL * kL * kL * kL * kL, kL * kL * kL * kL * kL * kL, kL * kL * kL * kL * kL * kL * kL, kL * kL * kL * kL * kL * kL * kL * kL)
        PL_kL2 = PL / kL2
        PL2_kL4 = PL_kL2 * PL_kL2
        PI = np.pi
        step = 6
        eps = 0.0026912
        kout = kL[::step] * (1.0 + eps)
        ko2, ko3, ko4, ko5, ko6, ko7, ko8 = (
         kout * kout, kout * kout * kout, kout * kout * kout * kout, kout * kout * kout * kout * kout, kout * kout * kout * kout * kout * kout, kout * kout * kout * kout * kout * kout * kout, kout * kout * kout * kout * kout * kout * kout * kout)
        if self.nz == 1:
            PLout = np.array([self.power_l_q(kout)])
        else:
            PLout = self.power_l_q(kout, self.z)
        dk = np.log(10) * np.log10(kL[1] / kL[0])
        dk2 = dk * dk
        ID = np.ones([len(kL)])
        IDo = ID[::step]
        P13f = []
        P22f = []
        P13 = np.zeros((self.nz, len(self.k_p)))
        P22 = np.zeros((self.nz, len(self.k_p)))
        for i in xrange(self.nz):
            A1, A2, A3, A4, A5, A6, A7 = (
             6 * np.outer(ID, ko8), 3 * np.outer(kL2, ko6), -45 * np.outer(kL4, ko4), 57 * np.outer(kL6, ko2), -21 * np.outer(kL8, IDo), np.arctanh(2 * np.outer(kL, kout) / np.add.outer(kL2, ko2)), np.outer(PL_kL2[i], IDo))
            B1, B2, B3, B4 = (12 * np.outer(PL[i] / kL, ko7), -158 * np.outer(PL[i] * kL, ko5), 100 * np.outer(PL[i] * kL3, ko3), -42 * np.outer(PL[i] * kL5, kout))
            integrand = B1 + B2 + B3 + B4 - (A1 + A2 + A3 + A4 + A5) * A6 * A7
            P13f.append(np.sum(integrand, axis=0))
            P13f[i] *= PI * dk * PLout[i] / 126.0 / ko3
            P13g = si.interp1d(kout, P13f[i], kind='cubic')
            P13[i] = P13g(self.k_p)

        p, q = np.meshgrid(kL, kL)
        for i in xrange(self.nz):
            Pp, Pq = np.meshgrid(PL[i], PL[i])
            pg, qg, Ppg, Pqg = (p[(p > q)], q[(p > q)], Pp[(p > q)], Pq[(p > q)])
            pg2, qg2, p2mq22, p2pq2, PpPq_2p2q2, pgpqg, pgmqg = (pg * pg, qg * qg, (pg * pg - qg * qg) * (pg * pg - qg * qg), pg * pg + qg * qg, Ppg * Pqg / (2 * pg * pg * qg * qg), pg + qg, pg - qg)
            P22f.append([ np.sum(PL2_kL4[(i, kkL >= K)] * (K * K + 3.0 * kL2[(kkL >= K)]) ** 2) + np.sum((2.0 * K * K - 5.0 * p2mq22[((K <= pgpqg) & (pgmqg <= K))] / (K * K) + 3.0 * p2pq2[((K <= pgpqg) & (pgmqg <= K))]) ** 2 * PpPq_2p2q2[((K <= pgpqg) & (pgmqg <= K))]) for K in kout ])
            P22f[i] *= PI * dk2 * ko3 / 49.0
            P22g = si.interp1d(kout, P22f[i], kind='cubic')
            P22[i] = P22g(self.k_p)

        self.Pk['1-3'] = P13
        self.Pk['2-2'] = P22
        self.Pk['1 loop'] = P13 + P22

    def Bk_TL(self, k1, k2, k3):
        """
                Tree-level bispectrum given the amplitude of the three 3-vectors.

                Parameters
                ----------

                'k1': float
                    Length of first vector.

                'k2': float
                    Length of second vector.

                'k3': float
                    Length of third vector.

                Returns
                ----------

                float
                """
        k_1_m = np.linalg.norm(k1)
        k_2_m = np.linalg.norm(k2)
        k_3_m = np.linalg.norm(k3)
        if self.nz == 1:
            power = si.interp1d(self.k_L, self.Pk_q, kind='linear')
            p1 = 2.0 * self.F_s(2, kk=[k1, k2]) * power(k_1_m) * power(k_2_m)
            p2 = 2.0 * self.F_s(2, kk=[k2, k3]) * power(k_2_m) * power(k_3_m)
            p3 = 2.0 * self.F_s(2, kk=[k3, k1]) * power(k_3_m) * power(k_1_m)
        else:
            power = si.interp2d(self.k_L, self.z, self.Pk_q, kind='linear')
            p1 = 2.0 * self.F_s(2, kk=[k1, k2]) * power(k_1_m, self.z) * power(k_2_m, self.z)
            p2 = 2.0 * self.F_s(2, kk=[k2, k3]) * power(k_2_m, self.z) * power(k_3_m, self.z)
            p3 = 2.0 * self.F_s(2, kk=[k3, k1]) * power(k_3_m, self.z) * power(k_1_m, self.z)
        return p1 + p2 + p3