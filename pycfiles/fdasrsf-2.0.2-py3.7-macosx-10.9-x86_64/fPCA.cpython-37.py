# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/fdasrsf/fPCA.py
# Compiled at: 2019-12-02 11:21:34
# Size of source mod 2**32: 16024 bytes
"""
Vertical and Horizontal Functional Principal Component Analysis using SRSF

moduleauthor:: Derek Tucker <jdtuck@sandia.gov>

"""
import numpy as np
import fdasrsf.utility_functions as uf
import fdasrsf.geometry as geo
from scipy import dot
from scipy.linalg import norm, svd
from scipy.integrate import trapz, cumtrapz
from scipy.optimize import fminbound
import matplotlib.pyplot as plt
import fdasrsf.plot_style as plot
import collections

class fdavpca:
    __doc__ = '\n    This class provides vertical fPCA using the\n    SRVF framework\n\n    Usage:  obj = fdavpca(warp_data)\n\n    :param warp_data: fdawarp class with alignment data\n    :param q_pca: srvf principal directions\n    :param f_pca: f principal directions\n    :param latent: latent values\n    :param coef: principal coefficients\n    :param id: point used for f(0)\n    :param mqn: mean srvf\n    :param U: eigenvectors\n    :param stds: geodesic directions\n\n    Author :  J. D. Tucker (JDT) <jdtuck AT sandia.gov>\n    Date   :  15-Mar-2018\n    '

    def __init__(self, fdawarp):
        """
        Construct an instance of the fdavpca class
        :param fdawarp: fdawarp class
        """
        if fdawarp.fn.size == 0:
            raise Exception('Please align fdawarp class using srsf_align!')
        self.warp_data = fdawarp

    def calc_fpca(self, no=3, id=None):
        """
        This function calculates vertical functional principal component analysis
        on aligned data

        :param no: number of components to extract (default = 3)
        :param id: point to use for f(0) (default = midpoint)
        :type no: int
        :type id: int

        :rtype: fdavpca object containing
        :return q_pca: srsf principal directions
        :return f_pca: functional principal directions
        :return latent: latent values
        :return coef: coefficients
        :return U: eigenvectors

        """
        fn = self.warp_data.fn
        time = self.warp_data.time
        qn = self.warp_data.qn
        M = time.shape[0]
        if id is None:
            mididx = int(np.round(M / 2))
        else:
            mididx = id
        coef = np.arange(-2.0, 3.0)
        Nstd = coef.shape[0]
        mq_new = qn.mean(axis=1)
        N = mq_new.shape[0]
        m_new = np.sign(fn[mididx, :]) * np.sqrt(np.abs(fn[mididx, :]))
        mqn = np.append(mq_new, m_new.mean())
        qn2 = np.vstack((qn, m_new))
        K = np.cov(qn2)
        U, s, V = svd(K)
        stdS = np.sqrt(s)
        q_pca = np.ndarray(shape=(N + 1, Nstd, no), dtype=float)
        for k in range(0, no):
            for l in range(0, Nstd):
                q_pca[:, l, k] = mqn + coef[l] * stdS[k] * U[:, k]

        f_pca = np.ndarray(shape=(N, Nstd, no), dtype=float)
        for k in range(0, no):
            for l in range(0, Nstd):
                f_pca[:, l, k] = uf.cumtrapzmid(time, q_pca[0:N, l, k] * np.abs(q_pca[0:N, l, k]), np.sign(q_pca[(N, l, k)]) * q_pca[(N, l, k)] ** 2, mididx)

            fbar = fn.mean(axis=1)
            fsbar = f_pca[:, :, k].mean(axis=1)
            err = np.transpose(np.tile(fbar - fsbar, (Nstd, 1)))
            f_pca[:, :, k] += err

        N2 = qn.shape[1]
        c = np.zeros((N2, no))
        for k in range(0, no):
            for l in range(0, N2):
                c[(l, k)] = sum((np.append(qn[:, l], m_new[l]) - mqn) * U[:, k])

        self.q_pca = q_pca
        self.f_pca = f_pca
        self.latent = s[0:no]
        self.coef = c
        self.U = U[:, 0:no]
        self.id = mididx
        self.mqn = mqn
        self.time = time
        self.stds = coef
        self.no = no

    def plot(self):
        """
        plot plot elastic vertical fPCA result
        Usage: obj.plot()
        """
        no = self.no
        Nstd = self.stds.shape[0]
        N = self.time.shape[0]
        num_plot = int(np.ceil(no / 3))
        CBcdict = {'Bl':(0, 0, 0), 
         'Or':(0.9, 0.6, 0), 
         'SB':(0.35, 0.7, 0.9), 
         'bG':(0, 0.6, 0.5), 
         'Ye':(0.95, 0.9, 0.25), 
         'Bu':(0, 0.45, 0.7), 
         'Ve':(0.8, 0.4, 0), 
         'rP':(0.8, 0.6, 0.7)}
        cl = sorted(CBcdict.keys())
        k = 0
        for ii in range(0, num_plot):
            if k > no - 1:
                break
            fig, ax = plt.subplots(2, 3)
            for k1 in range(0, 3):
                k = k1 + ii * 3
                axt = ax[(0, k1)]
                if k > no - 1:
                    break
                for l in range(0, Nstd):
                    axt.plot((self.time), (self.q_pca[0:N, l, k]), color=(CBcdict[cl[l]]))

                axt.set_title('q domain: PD %d' % (k + 1))
                axt = ax[(1, k1)]
                for l in range(0, Nstd):
                    axt.plot((self.time), (self.f_pca[:, l, k]), color=(CBcdict[cl[l]]))

                axt.set_title('f domain: PD %d' % (k + 1))

            fig.set_tight_layout(True)

        cumm_coef = 100 * np.cumsum(self.latent) / sum(self.latent)
        N = self.latent.shape[0]
        idx = np.arange(0, N) + 1
        plot.f_plot(idx, cumm_coef, 'Coefficient Cumulative Percentage')
        plt.xlabel('Percentage')
        plt.ylabel('Index')
        plt.show()


class fdahpca:
    __doc__ = '\n    This class provides horizontal fPCA using the\n    SRVF framework\n\n    Usage:  obj = fdahpca(warp_data)\n\n    :param warp_data: fdawarp class with alignment data\n    :param gam_pca: warping functions principal directions\n    :param psi_pca: srvf principal directions\n    :param latent: latent values\n    :param U: eigenvectors\n    :param coef: coeficients\n    :param vec: shooting vectors\n    :param mu: Karcher Mean\n    :param tau: principal directions\n\n    Author :  J. D. Tucker (JDT) <jdtuck AT sandia.gov>\n    Date   :  15-Mar-2018\n    '

    def __init__(self, fdawarp):
        """
        Construct an instance of the fdavpca class
        :param fdawarp: fdawarp class
        """
        if fdawarp.fn.size == 0:
            raise Exception('Please align fdawarp class using srsf_align!')
        self.warp_data = fdawarp

    def calc_fpca(self, no=3):
        """
        This function calculates horizontal functional principal component analysis on aligned data

        :param no: number of components to extract (default = 3)
        :type no: int

        :rtype: fdahpca object of numpy ndarray
        :return q_pca: srsf principal directions
        :return f_pca: functional principal directions
        :return latent: latent values
        :return coef: coefficients
        :return U: eigenvectors

        """
        gam = self.warp_data.gam
        mu, gam_mu, psi, vec = uf.SqrtMean(gam)
        tau = np.arange(1, 6)
        TT = self.warp_data.time.shape[0]
        K = np.cov(vec)
        U, s, V = svd(K)
        vm = vec.mean(axis=1)
        gam_pca = np.ndarray(shape=(tau.shape[0], mu.shape[0], no), dtype=float)
        psi_pca = np.ndarray(shape=(tau.shape[0], mu.shape[0], no), dtype=float)
        for j in range(0, no):
            for k in tau:
                v = (k - 3) * np.sqrt(s[j]) * U[:, j]
                vn = norm(v) / np.sqrt(TT)
                if vn < 0.0001:
                    psi_pca[k - 1, :, j] = mu
                else:
                    psi_pca[k - 1, :, j] = np.cos(vn) * mu + np.sin(vn) * v / vn
                tmp = cumtrapz((psi_pca[k - 1, :, j] * psi_pca[k - 1, :, j]), (np.linspace(0, 1, TT)), initial=0)
                gam_pca[k - 1, :, j] = (tmp - tmp[0]) / (tmp[(-1)] - tmp[0])

        N2 = gam.shape[1]
        c = np.zeros((N2, no))
        for k in range(0, no):
            for i in range(0, N2):
                c[(i, k)] = np.sum(dot(vec[:, i] - vm, U[:, k]))

        self.gam_pca = gam_pca
        self.psi_pca = psi_pca
        self.U = U
        self.coef = c
        self.latent = s
        self.gam_mu = gam_mu
        self.psi_mu = mu
        self.vec = vec
        self.no = no

    def plot(self):
        """
        plot plot elastic horizontal fPCA results

        Usage: obj.plot()
        """
        no = self.no
        TT = self.warp_data.time.shape[0]
        num_plot = int(np.ceil(no / 3))
        CBcdict = {'Bl':(0, 0, 0), 
         'Or':(0.9, 0.6, 0), 
         'SB':(0.35, 0.7, 0.9), 
         'bG':(0, 0.6, 0.5), 
         'Ye':(0.95, 0.9, 0.25), 
         'Bu':(0, 0.45, 0.7), 
         'Ve':(0.8, 0.4, 0), 
         'rP':(0.8, 0.6, 0.7)}
        k = 0
        for ii in range(0, num_plot):
            if k > no - 1:
                break
            fig, ax = plt.subplots(1, 3)
            for k1 in range(0, 3):
                k = k1 + ii * 3
                axt = ax[k1]
                if k > no - 1:
                    break
                tmp = self.gam_pca[:, :, k]
                axt.plot(np.linspace(0, 1, TT), tmp.transpose())
                axt.set_title('PD %d' % (k + 1))
                axt.set_aspect('equal')

            fig.set_tight_layout(True)

        cumm_coef = 100 * np.cumsum(self.latent[0:no]) / sum(self.latent[0:no])
        idx = np.arange(0, no) + 1
        plot.f_plot(idx, cumm_coef, 'Coefficient Cumulative Percentage')
        plt.xlabel('Percentage')
        plt.ylabel('Index')
        plt.show()


class fdajpca:
    __doc__ = '\n    This class provides joint fPCA using the\n    SRVF framework\n\n    Usage:  obj = fdajpca(warp_data)\n\n    :param warp_data: fdawarp class with alignment data\n    :param q_pca: srvf principal directions\n    :param f_pca: f principal directions\n    :param latent: latent values\n    :param coef: principal coefficients\n    :param id: point used for f(0)\n    :param mqn: mean srvf\n    :param U: eigenvectors\n    :param mu_psi: mean psi\n    :param mu_g: mean g\n    :param C: scaling value\n    :param stds: geodesic directions\n\n    Author :  J. D. Tucker (JDT) <jdtuck AT sandia.gov>\n    Date   :  18-Mar-2018\n    '

    def __init__(self, fdawarp):
        """
        Construct an instance of the fdavpca class
        :param fdawarp: fdawarp class
        """
        if fdawarp.fn.size == 0:
            raise Exception('Please align fdawarp class using srsf_align!')
        self.warp_data = fdawarp

    def calc_fpca(self, no=3, id=None):
        """
        This function calculates joint functional principal component analysis
        on aligned data

        :param no: number of components to extract (default = 3)
        :param id: point to use for f(0) (default = midpoint)
        :type no: int
        :type id: int

        :rtype: fdajpca object of numpy ndarray
        :return q_pca: srsf principal directions
        :return f_pca: functional principal directions
        :return latent: latent values
        :return coef: coefficients
        :return U: eigenvectors

        """
        fn = self.warp_data.fn
        time = self.warp_data.time
        qn = self.warp_data.qn
        q0 = self.warp_data.q0
        gam = self.warp_data.gam
        M = time.shape[0]
        if id is None:
            mididx = int(np.round(M / 2))
        else:
            mididx = id
        coef = np.arange(-1.0, 2.0)
        Nstd = coef.shape[0]
        mq_new = qn.mean(axis=1)
        m_new = np.sign(fn[mididx, :]) * np.sqrt(np.abs(fn[mididx, :]))
        mqn = np.append(mq_new, m_new.mean())
        qn2 = np.vstack((qn, m_new))
        mu_psi, gam_mu, psi, vec = uf.SqrtMean(gam)
        C = fminbound(find_C, 0, 10000.0, (qn2, vec, q0, no, mu_psi))
        qhat, gamhat, a, U, s, mu_g, g, cov = jointfPCAd(qn2, vec, C, no, mu_psi)
        q_pca = np.ndarray(shape=(M, Nstd, no), dtype=float)
        f_pca = np.ndarray(shape=(M, Nstd, no), dtype=float)
        for k in range(0, no):
            for l in range(0, Nstd):
                qhat = mqn + dot(U[0:M + 1, k], coef[l] * np.sqrt(s[k]))
                vechat = dot(U[M + 1:, k], coef[l] * np.sqrt(s[k]) / C)
                psihat = geo.exp_map(mu_psi, vechat)
                gamhat = cumtrapz((psihat * psihat), (np.linspace(0, 1, M)), initial=0)
                gamhat = (gamhat - gamhat.min()) / (gamhat.max() - gamhat.min())
                if sum(vechat) == 0:
                    gamhat = np.linspace(0, 1, M)
                fhat = uf.cumtrapzmid(time, qhat[0:M] * np.fabs(qhat[0:M]), np.sign(qhat[M]) * (qhat[M] * qhat[M]), mididx)
                f_pca[:, l, k] = uf.warp_f_gamma(np.linspace(0, 1, M), fhat, gamhat)
                q_pca[:, l, k] = uf.warp_q_gamma(np.linspace(0, 1, M), qhat[0:M], gamhat)

        self.q_pca = q_pca
        self.f_pca = f_pca
        self.latent = s
        self.coef = a
        self.U = U
        self.mu_psi = mu_psi
        self.mu_g = mu_g
        self.id = mididx
        self.C = C
        self.time = time
        self.g = g
        self.cov = cov
        self.no = no
        self.stds = coef

    def plot(self):
        """
        plot plot elastic vertical fPCA result

        Usage: obj.plot()
        """
        no = self.no
        M = self.time.shape[0]
        Nstd = self.stds.shape[0]
        num_plot = int(np.ceil(no / 3))
        CBcdict = {'Bl':(0, 0, 0), 
         'Or':(0.9, 0.6, 0), 
         'SB':(0.35, 0.7, 0.9), 
         'bG':(0, 0.6, 0.5), 
         'Ye':(0.95, 0.9, 0.25), 
         'Bu':(0, 0.45, 0.7), 
         'Ve':(0.8, 0.4, 0), 
         'rP':(0.8, 0.6, 0.7)}
        cl = sorted(CBcdict.keys())
        k = 0
        for ii in range(0, num_plot):
            if k > no - 1:
                break
            fig, ax = plt.subplots(2, 3)
            for k1 in range(0, 3):
                k = k1 + ii * 3
                axt = ax[(0, k1)]
                if k > no - 1:
                    break
                for l in range(0, Nstd):
                    axt.plot((self.time), (self.q_pca[0:M, l, k]), color=(CBcdict[cl[l]]))

                axt.set_title('q domain: PD %d' % (k + 1))
                axt = ax[(1, k1)]
                for l in range(0, Nstd):
                    axt.plot((self.time), (self.f_pca[:, l, k]), color=(CBcdict[cl[l]]))

                axt.set_title('f domain: PD %d' % (k + 1))

            fig.set_tight_layout(True)

        cumm_coef = 100 * np.cumsum(self.latent) / sum(self.latent)
        idx = np.arange(0, self.latent.shape[0]) + 1
        plot.f_plot(idx, cumm_coef, 'Coefficient Cumulative Percentage')
        plt.xlabel('Percentage')
        plt.ylabel('Index')
        plt.show()


def jointfPCAd(qn, vec, C, m, mu_psi):
    M, N = qn.shape
    g = np.vstack((qn, C * vec))
    mu_q = qn.mean(axis=1)
    mu_g = g.mean(axis=1)
    K = np.cov(g)
    U, s, V = svd(K)
    a = np.zeros((N, m))
    for i in range(0, N):
        for j in range(0, m):
            tmp = g[:, i] - mu_g
            a[(i, j)] = dot(tmp.T, U[:, j])

    qhat = np.tile(mu_q, (N, 1))
    qhat = qhat.T
    qhat = qhat + dot(U[0:M, 0:m], a.T)
    vechat = dot(U[M:, 0:m], a.T / C)
    psihat = np.zeros((M - 1, N))
    gamhat = np.zeros((M - 1, N))
    for ii in range(0, N):
        psihat[:, ii] = geo.exp_map(mu_psi, vechat[:, ii])
        gam_tmp = cumtrapz((psihat[:, ii] * psihat[:, ii]), (np.linspace(0, 1, M - 1)), initial=0)
        gamhat[:, ii] = (gam_tmp - gam_tmp.min()) / (gam_tmp.max() - gam_tmp.min())

    U = U[:, 0:m]
    s = s[0:m]
    return (
     qhat, gamhat, a, U, s, mu_g, g, K)


def find_C(C, qn, vec, q0, m, mu_psi):
    qhat, gamhat, a, U, s, mu_g, g, K = jointfPCAd(qn, vec, C, m, mu_psi)
    M, N = qn.shape
    time = np.linspace(0, 1, M - 1)
    d = np.zeros(N)
    for i in range(0, N):
        tmp = uf.warp_q_gamma(time, qhat[0:M - 1, i], uf.invertGamma(gamhat[:, i]))
        d[i] = trapz((tmp - q0[:, i]) * (tmp - q0[:, i]), time)

    out = sum(d * d) / N
    return out