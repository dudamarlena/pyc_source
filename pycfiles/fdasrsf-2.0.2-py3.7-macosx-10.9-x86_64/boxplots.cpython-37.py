# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/fdasrsf/boxplots.py
# Compiled at: 2019-10-14 10:32:19
# Size of source mod 2**32: 18268 bytes
"""
Elastic Functional Boxplots

moduleauthor:: Derek Tucker <jdtuck@sandia.gov>

"""
import numpy as np
from scipy.integrate import trapz
import fdasrsf.utility_functions as uf
import fdasrsf.geometry as geo
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import collections

class ampbox:
    __doc__ = '\n    This class provides amplitude boxplot for functional data using the\n    SRVF framework\n    \n    Usage:  obj = ampbox(warp_data)\n    \n    :param warp_data: fdawarp class with alignment data\n    :type warp_data: fdawarp\n    :param Q1: First quartile\n    :param Q3: Second quartile\n    :param Q1a: First quantile based on alpha\n    :param Q3a: Second quantile based on alpha\n    :param minn: minimum extreme function\n    :param maxx: maximum extreme function\n    :param outlier_index: indexes of outlier functions\n    :param f_median: median function\n    :param q_median: median srvf\n    :param plt: surface plot mesh\n    \n    Author :  J. D. Tucker (JDT) <jdtuck AT sandia.gov>\n    Date   :  15-Mar-2018\n    '

    def __init__(self, fdawarp):
        """
        Construct an instance of the ampbox class
        :param fdawarp: fdawarp class
        """
        if fdawarp.fn.size == 0:
            raise Exception('Please align fdawarp class using srsf_align!')
        if fdawarp.type == 'mean':
            raise Exception('Please align fdawarp class using srsf_align with method="median"!')
        self.warp_data = fdawarp

    def construct_boxplot(self, alpha=0.05, k_a=1):
        r"""
        This function constructs the amplitude boxplot using the elastic
        square-root slope (srsf) framework.

        :param alpha: quantile value (e.g.,=.05, i.e., 95\%)
        :param k_a: scalar for outlier cutoff (e.g.,=1)
        """
        if self.warp_data.rsamps:
            ft = self.warp_data.fs
            f_median = self.warp_data.fmean
            qt = self.warp_data.qs
            q_median = self.warp_data.mqn
            time = self.warp_data.time
        else:
            ft = self.warp_data.fn
            f_median = self.warp_data.fmean
            qt = self.warp_data.qn
            q_median = self.warp_data.mqn
            time = self.warp_data.time
        N = ft.shape[1]
        lam = 0.5
        dy = np.zeros(N)
        for i in range(0, N):
            dy[i] = np.sqrt(trapz((q_median - qt[:, i]) ** 2, time))

        dy_ordering = dy.argsort()
        CR_50 = dy_ordering[0:np.ceil(N / 2).astype('int')]
        tmp = dy[CR_50]
        m = tmp.max()
        angle = np.zeros((CR_50.shape[0], CR_50.shape[0]))
        energy = np.zeros((CR_50.shape[0], CR_50.shape[0]))
        for i in range(0, CR_50.shape[0] - 1):
            for j in range(i + 1, CR_50.shape[0]):
                q1 = qt[:, CR_50[i]] - q_median
                q3 = qt[:, CR_50[j]] - q_median
                q1 = q1 / np.sqrt(trapz(q1 ** 2, time))
                q3 = q3 / np.sqrt(trapz(q3 ** 2, time))
                angle[(i, j)] = trapz(q1 * q3, time)
                energy[(i, j)] = (1 - lam) * (dy[CR_50[i]] / m + dy[CR_50[j]] / m) - lam * (angle[(i, j)] + 1)

        maxloc = energy.argmax()
        maxloc_row, maxloc_col = np.unravel_index(maxloc, energy.shape)
        Q1_index = CR_50[maxloc_row]
        Q3_index = CR_50[maxloc_col]
        Q1_q = qt[:, Q1_index]
        Q3_q = qt[:, Q3_index]
        Q1 = ft[:, Q1_index]
        Q3 = ft[:, Q3_index]
        dy_ordering = dy.argsort()
        CR_alpha = dy_ordering[0:np.round(N * (1 - alpha)).astype('int')]
        tmp = dy[CR_alpha]
        m = tmp.max()
        angle = np.zeros((CR_alpha.shape[0], CR_alpha.shape[0]))
        energy = np.zeros((CR_alpha.shape[0], CR_alpha.shape[0]))
        for i in range(0, CR_alpha.shape[0] - 1):
            for j in range(i + 1, CR_alpha.shape[0]):
                q1 = qt[:, CR_alpha[i]] - q_median
                q3 = qt[:, CR_alpha[j]] - q_median
                q1 /= np.sqrt(trapz(q1 ** 2, time))
                q3 /= np.sqrt(trapz(q3 ** 2, time))
                angle[(i, j)] = trapz(q1 * q3, time)
                energy[(i, j)] = (1 - lam) * (dy[CR_alpha[i]] / m + dy[CR_alpha[j]] / m) - lam * (angle[(i, j)] + 1)

        maxloc = energy.argmax()
        maxloc_row, maxloc_col = np.unravel_index(maxloc, energy.shape)
        Q1a_index = CR_alpha[maxloc_row]
        Q3a_index = CR_alpha[maxloc_col]
        Q1a_q = qt[:, Q1a_index]
        Q3a_q = qt[:, Q3a_index]
        Q1a = ft[:, Q1a_index]
        Q3a = ft[:, Q3a_index]
        IQR = dy[Q1_index] + dy[Q3_index]
        v1 = Q1_q - q_median
        v3 = Q3_q - q_median
        upper_q = Q3_q + k_a * IQR * v3 / np.sqrt(trapz(v3 ** 2, time))
        lower_q = Q1_q + k_a * IQR * v1 / np.sqrt(trapz(v1 ** 2, time))
        upper_dis = np.sqrt(trapz((upper_q - q_median) ** 2, time))
        lower_dis = np.sqrt(trapz((lower_q - q_median) ** 2, time))
        whisker_dis = max(upper_dis, lower_dis)
        outlier_index = np.array([])
        for i in range(0, N):
            if dy[dy_ordering[(N - i - 1)]] > whisker_dis:
                outlier_index = np.append(outlier_index, dy[dy_ordering[(N + 1 - i)]])

        distance_to_upper = np.full(N, np.inf)
        distance_to_lower = np.full(N, np.inf)
        out_50_CR = np.setdiff1d(np.arange(0, N), outlier_index)
        for i in range(0, out_50_CR.shape[0]):
            j = out_50_CR[i]
            distance_to_upper[j] = np.sqrt(trapz((upper_q - qt[:, j]) ** 2, time))
            distance_to_lower[j] = np.sqrt(trapz((lower_q - qt[:, j]) ** 2, time))

        max_index = distance_to_upper.argmin()
        min_index = distance_to_lower.argmin()
        min_q = qt[:, min_index]
        max_q = qt[:, max_index]
        minn = ft[:, min_index]
        maxx = ft[:, max_index]
        s = np.linspace(0, 1, 100)
        Fs2 = np.zeros((time.shape[0], 595))
        Fs2[:, 0] = (1 - s[0]) * minn + s[0] * Q1
        for j in range(1, 100):
            Fs2[:, j] = (1 - s[j]) * minn + s[j] * Q1a
            Fs2[:, 98 + j] = (1 - s[j]) * Q1a + s[j] * Q1
            Fs2[:, 197 + j] = (1 - s[j]) * Q1 + s[j] * f_median
            Fs2[:, 296 + j] = (1 - s[j]) * f_median + s[j] * Q3
            Fs2[:, 395 + j] = (1 - s[j]) * Q3 + s[j] * Q3a
            Fs2[:, 494 + j] = (1 - s[j]) * Q3a + s[j] * maxx

        d1 = np.sqrt(trapz((q_median - Q1_q) ** 2, time))
        d1a = np.sqrt(trapz((Q1_q - Q1a_q) ** 2, time))
        dl = np.sqrt(trapz((Q1a_q - min_q) ** 2, time))
        d3 = np.sqrt(trapz((q_median - Q3_q) ** 2, time))
        d3a = np.sqrt(trapz((Q3_q - Q3a_q) ** 2, time))
        du = np.sqrt(trapz((Q3a_q - max_q) ** 2, time))
        part1 = np.linspace(-d1 - d1a - dl, -d1 - d1a, 100)
        part2 = np.linspace(-d1 - d1a, -d1, 100)
        part3 = np.linspace(-d1, 0, 100)
        part4 = np.linspace(0, d3, 100)
        part5 = np.linspace(d3, d3 + d3a, 100)
        part6 = np.linspace(d3 + d3a, d3 + d3a + du, 100)
        allparts = np.hstack((part1, part2[1:100], part3[1:100], part4[1:100], part5[1:100], part6[1:100]))
        U, V = np.meshgrid(time, allparts)
        U = np.transpose(U)
        V = np.transpose(V)
        self.Q1 = Q1
        self.Q3 = Q3
        self.Q1a = Q1a
        self.Q3a = Q3a
        self.minn = minn
        self.maxx = maxx
        self.outlier_index = outlier_index
        self.f_median = f_median
        self.q_median = q_median
        plt = collections.namedtuple('plt', ['U', 'V', 'Fs2', 'allparts',
         'd1', 'd1a', 'dl',
         'd3', 'd3a', 'du',
         'Q1q', 'Q3q'])
        self.plt = plt(U, V, Fs2, allparts, d1, d1a, dl, d3, d3a, du, Q1a_q, Q3a_q)


class phbox:
    __doc__ = '\n    This class provides phase boxplot for functional data using the\n    SRVF framework\n    \n    Usage:  obj = phbox(warp_data)\n    \n    :param warp_data: fdawarp class with alignment data\n    :type warp_data: fdawarp\n    :param Q1: First quartile\n    :param Q3: Second quartile\n    :param Q1a: First quantile based on alpha\n    :param Q3a: Second quantile based on alpha\n    :param minn: minimum extreme function\n    :param maxx: maximum extreme function\n    :param outlier_index: indexes of outlier functions\n    :param median_x: median warping function\n    :param psi_median: median srvf of warping function\n    :param plt: surface plot mesh\n    \n    Author :  J. D. Tucker (JDT) <jdtuck AT sandia.gov>\n    Date   :  15-Mar-2018\n    '

    def __init__(self, fdawarp):
        """
        Construct an instance of the phbox class
        :param fdawarp: fdawarp class
        """
        if fdawarp.fn.size == 0:
            raise Exception('Please align fdawarp class using srsf_align!')
        if fdawarp.type == 'mean':
            raise Exception('Please align fdawarp class using srsf_align with method="median"!')
        self.warp_data = fdawarp

    def construct_boxplot(self, alpha=0.05, k_a=1):
        r"""
        This function constructs phase boxplot for functional data using the elastic
        square-root slope (srsf) framework.

        :param alpha: quantile value (e.g.,=.05, i.e., 95\%)
        :param k_a: scalar for outlier cutoff (e.g.,=1)
        """
        if self.warp_data.rsamps:
            gam = self.warp_data.gams
        else:
            gam = self.warp_data.gam
        M, N = gam.shape
        t = np.linspace(0, 1, M)
        time = t
        lam = 0.5
        median_x, psi_median, psi, vec = uf.SqrtMedian(gam)
        dx = np.zeros(N)
        v = np.zeros((M, N))
        for k in range(0, N):
            v[:, k], d = geo.inv_exp_map(psi_median, psi[:, k])
            dx[k] = np.sqrt(trapz(v[:, k] ** 2, t))

        dx_ordering = dx.argsort()
        CR_50 = dx_ordering[0:np.ceil(N / 2).astype('int')]
        tmp = dx[CR_50]
        m = tmp.max()
        angle = np.zeros((CR_50.shape[0], CR_50.shape[0]))
        energy = np.zeros((CR_50.shape[0], CR_50.shape[0]))
        for i in range(0, CR_50.shape[0] - 1):
            for j in range(i + 1, CR_50.shape[0]):
                q1 = v[:, CR_50[i]]
                q3 = v[:, CR_50[j]]
                q1 /= np.sqrt(trapz(q1 ** 2, time))
                q3 /= np.sqrt(trapz(q3 ** 2, time))
                angle[(i, j)] = trapz(q1 * q3, time)
                energy[(i, j)] = (1 - lam) * (dx[CR_50[i]] / m + dx[CR_50[j]] / m) - lam * (angle[(i, j)] + 1)

        maxloc = energy.argmax()
        maxloc_row, maxloc_col = np.unravel_index(maxloc, energy.shape)
        Q1_index = CR_50[maxloc_row]
        Q3_index = CR_50[maxloc_col]
        Q1 = gam[:, Q1_index]
        Q3 = gam[:, Q3_index]
        Q1_psi = np.sqrt(np.gradient(Q1, 1 / (M - 1)))
        Q3_psi = np.sqrt(np.gradient(Q3, 1 / (M - 1)))
        dx_ordering = dx.argsort()
        CR_alpha = dx_ordering[0:np.round(N * (1 - alpha)).astype('int')]
        tmp = dx[CR_alpha]
        m = tmp.max()
        angle = np.zeros((CR_alpha.shape[0], CR_alpha.shape[0]))
        energy = np.zeros((CR_alpha.shape[0], CR_alpha.shape[0]))
        for i in range(0, CR_alpha.shape[0] - 1):
            for j in range(i + 1, CR_alpha.shape[0]):
                q1 = v[:, CR_alpha[i]]
                q3 = v[:, CR_alpha[j]]
                q1 /= np.sqrt(trapz(q1 ** 2, time))
                q3 /= np.sqrt(trapz(q3 ** 2, time))
                angle[(i, j)] = trapz(q1 * q3, time)
                energy[(i, j)] = (1 - lam) * (dx[CR_alpha[i]] / m + dx[CR_alpha[j]] / m) - lam * (angle[(i, j)] + 1)

        maxloc = energy.argmax()
        maxloc_row, maxloc_col = np.unravel_index(maxloc, energy.shape)
        Q1a_index = CR_alpha[maxloc_row]
        Q3a_index = CR_alpha[maxloc_col]
        Q1a = gam[:, Q1a_index]
        Q3a = gam[:, Q3a_index]
        Q1a_psi = np.sqrt(np.gradient(Q1a, 1 / (M - 1)))
        Q3a_psi = np.sqrt(np.gradient(Q3a, 1 / (M - 1)))
        tst = trapz(v[:, Q1a_index] * v[:, Q1_index])
        if tst < 0:
            Q1a = gam[:, Q3a_index]
            Q3a = gam[:, Q1a_index]
        IQR = dx[Q1_index] + dx[Q3_index]
        v1 = v[:, Q3a_index]
        v3 = v[:, Q3a_index]
        upper_v = v3 + k_a * IQR * v3 / np.sqrt(trapz(v3 ** 2, time))
        lower_v = v1 + k_a * IQR * v1 / np.sqrt(trapz(v1 ** 2, time))
        upper_dis = np.sqrt(trapz(v3 ** 2, time))
        lower_dis = np.sqrt(trapz(v1 ** 2, time))
        whisker_dis = max(upper_dis, lower_dis)
        outlier_index = np.array([])
        for i in range(0, N):
            if dx[dx_ordering[(N - 1 - i)]] > whisker_dis:
                outlier_index = np.append(outlier_index, dx_ordering[(N + 1 - i)])

        distance_to_upper = np.full(N, np.inf)
        distance_to_lower = np.full(N, np.inf)
        out_50_CR = np.setdiff1d(np.arange(0, N), outlier_index)
        for i in range(0, out_50_CR.shape[0]):
            j = out_50_CR[i]
            distance_to_upper[j] = np.sqrt(trapz((upper_v - v[:, j]) ** 2, time))
            distance_to_lower[j] = np.sqrt(trapz((lower_v - v[:, j]) ** 2, time))

        max_index = distance_to_upper.argmin()
        min_index = distance_to_lower.argmin()
        minn = gam[:, min_index]
        maxx = gam[:, max_index]
        min_psi = psi[:, min_index]
        max_psi = psi[:, max_index]
        s = np.linspace(0, 1, 100)
        Fs2 = np.zeros((time.shape[0], 595))
        Fs2[:, 0] = (1 - s[0]) * (minn - t) + s[0] * (Q1 - t)
        for j in range(1, 100):
            Fs2[:, j] = (1 - s[j]) * (minn - t) + s[j] * (Q1a - t)
            Fs2[:, 98 + j] = (1 - s[j]) * (Q1a - t) + s[j] * (Q1 - t)
            Fs2[:, 197 + j] = (1 - s[j]) * (Q1 - t) + s[j] * (median_x - t)
            Fs2[:, 296 + j] = (1 - s[j]) * (median_x - t) + s[j] * (Q3 - t)
            Fs2[:, 395 + j] = (1 - s[j]) * (Q3 - t) + s[j] * (Q3a - t)
            Fs2[:, 494 + j] = (1 - s[j]) * (Q3a - t) + s[j] * (maxx - t)

        d1 = np.sqrt(trapz(psi_median * Q1_psi, time))
        d1a = np.sqrt(trapz(Q1_psi * Q1a_psi, time))
        dl = np.sqrt(trapz(Q1a_psi * min_psi, time))
        d3 = np.sqrt(trapz(psi_median * Q3_psi, time))
        d3a = np.sqrt(trapz(Q3_psi * Q3a_psi, time))
        du = np.sqrt(trapz(Q3a_psi * max_psi, time))
        part1 = np.linspace(-d1 - d1a - dl, -d1 - d1a, 100)
        part2 = np.linspace(-d1 - d1a, -d1, 100)
        part3 = np.linspace(-d1, 0, 100)
        part4 = np.linspace(0, d3, 100)
        part5 = np.linspace(d3, d3 + d3a, 100)
        part6 = np.linspace(d3 + d3a, d3 + d3a + du, 100)
        allparts = np.hstack((part1, part2[1:100], part3[1:100], part4[1:100], part5[1:100], part6[1:100]))
        U, V = np.meshgrid(time, allparts)
        U = np.transpose(U)
        V = np.transpose(V)
        self.Q1 = Q1
        self.Q3 = Q3
        self.Q1a = Q1a
        self.Q3a = Q3a
        self.minn = minn
        self.maxx = maxx
        self.outlier_index = outlier_index
        self.median_x = median_x
        self.psi_media = psi_median
        plt = collections.namedtuple('plt', ['U', 'V', 'Fs2', 'allparts',
         'd1', 'd1a', 'dl',
         'd3', 'd3a', 'du',
         'Q1_psi', 'Q3_psi'])
        self.plt = plt(U, V, Fs2, allparts, d1, d1a, dl, d3, d3a, du, Q1a_psi, Q3a_psi)

    def plot(self):
        """
        plot box plot and surface plot

        Usage: obj.plot()
        """
        M = self.warp_data.time.shape[0]
        time = np.linspace(0, 1, M)
        fig1, ax1 = plt.subplots()
        ax1.plot(time, self.median_x, 'k')
        ax1.plot(time, self.Q1, 'b')
        ax1.plot(time, self.Q3, 'b')
        ax1.plot(time, self.Q1a, 'g')
        ax1.plot(time, self.Q3a, 'g')
        ax1.plot(time, self.minn, 'r')
        ax1.plot(time, self.maxx, 'r')
        ax1.set_aspect('equal')
        fig2 = plt.figure()
        ax = fig2.gca(projection='3d')
        ax.plot_surface((self.plt.U), (self.plt.V), (self.plt.Fs2), cmap=(cm.viridis), rcount=200, ccount=200)
        ax.plot(time, np.zeros(M), self.median_x - time, 'k')
        ax.plot(time, np.repeat(-self.plt.d1, M), self.Q1 - time, 'b')
        ax.plot(time, np.repeat(-self.plt.d1 - self.plt.d1a, M), self.Q1a - time, 'g')
        ax.plot(time, np.repeat(-self.plt.d1 - self.plt.d1a - self.plt.dl, M), self.minn - time, 'r')
        ax.plot(time, np.repeat(self.plt.d3, M), self.Q3 - time, 'b')
        ax.plot(time, np.repeat(self.plt.d3 + self.plt.d3a, M), self.Q3a - time, 'g')
        ax.plot(time, np.repeat(self.plt.d3 + self.plt.d3a + self.plt.du, M), self.maxx - time, 'r')
        plt.show()