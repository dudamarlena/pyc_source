# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gentex/texmeas.py
# Compiled at: 2019-10-04 13:17:54
# Size of source mod 2**32: 29968 bytes
"""  gentex.texmeas package

"""
import numpy as np

class Texmeas:
    __doc__ = "Class texmeas for generating texture measures from co-occurrence matrix\n\n    Parameters\n    ----------\n\n    comat: ndarray\n        Non-normalized co-occurrence matrix - chi-squared conditional distribution\n        comparisons require the actual number of counts so don't normalize this before\n        sending in\n\n    measure: string\n        Texture measure (default = 'Statistical Complexity'). Choice of:\n\n            * 'CM Entropy'\n            * 'EM Entropy'\n            * 'Statistical Complexity'\n            * 'Energy Uniformity'\n            * 'Maximum Probability'\n            * 'Contrast'\n            * 'Inverse Difference Moment'\n            * 'Correlation'\n            * 'Probability of Run Length'\n            * 'Epsilon Machine Run Length'\n            * 'Run Length Asymmetry'\n            * 'Homogeneity'\n            * 'Cluster Tendency'\n            * 'Multifractal Spectrum Energy Range'\n            * 'Multifractal Spectrum Entropy Range'\n\n    coordmo: int\n        Moment of coordinate differences in co-occurrence matrix\n        needed for calculating 'Contrast' and 'Inverse Difference Moment'  (default=0)\n\n    probmom: int\n        Moment of individual cooccurence probabilities\n        needed for calculating 'Contrast' and 'Inverse Difference Moment'  (default=0)\n\n    rllen: int\n        Length of run length used for generating probability\n        of a run length (the higher this probability the\n        larger the constant patches on the scale used for generating\n        the co-occurence matrix) or the epsilon machine run length  (default=0)\n\n    clusmom: int\n        Moment used for generating cooccurence cluster tendency (default=0)\n               \n    samelev: bool\n        Whether to treat the rows and columns in the cooccurence\n        matrix as identical 'states' (the methods are very general\n        so this needn't be the case, e.g. different template shapes\n        from different images with different quantization levels\n        could be used to generate the cooccurence matrix which could\n        be of arbitrary shape)\n\n        default = True assumes the cooccurrence matrix is square\n        and the rows and columns correspond to the same 'state'\n\n    betas: array\n        An array of 3 values, the lower limit, the upper limit and\n        the number of steps to use as the 'inverse temperature' range\n        for estimating the multifractal spectrum from an epsilon machine\n        - getting the range right for an 'arbitrary' epsilon machine is\n        tricky and is expected to be reset over a number of trials before\n        getting a full spectrum estimate. For details on the rationale\n        and algorithm see:\n\n        K. Young and J. P. Crutchfield, 'Fluctuation Spectroscopy',\n        Chaos, Solitons, and Fractals 4 (1993) 5-39.\n\n\n    Attributes\n    ----------\n\n    emclus: int\n        Number of clusters ('states') found when estimating an epsilon machine from the co-occurrence matrix.\n\n    emest: bool\n        Whether or not an epsilon machine has been estimated yet\n\n    emmat: float\n        The estimated epsilon machine as a standard Markov process transition matrix.\n\n    condo: 2d-array\n        Co-occurrence matrix renormalized as a rowise matrix of conditional probabilites - built as part of\n        epsilon machine estimation\n\n    emclasses: list\n        List of which of the values in emclus each row in condo (and hence the cooccurence matrix) belongs to\n\n    clusp: float\n        Chisquared p value to use for clustering epsilon machine rows\n\n    val: float\n        Value of most recently calculated texture measure\n\n    mfsspec: array\n        Array containing the multifractal spectral estimates obtained\n        over the range of 'inverse temperatures' provided in betas\n\n    currval: string\n        One of the listed measures method which constitutes the current value in val\n            \n    "

    def __init__(self, comat, measure='Statistical Complexity', coordmom=0, probmom=0, rllen=0, clusmom=0, clusp=0.001, samelev=True, betas=[-20, 20, 40]):
        self.comat = comat
        self.totcount = np.sum(comat)
        self.measure = measure
        self.coordmom = coordmom
        self.probmom = probmom
        self.rllen = rllen
        self.clusmom = clusmom
        self.clusp = clusp
        self.emclus = 0
        self.emest = False
        self.mfsest = False
        self.emmat = np.array([])
        self.condo = np.array([])
        self.emclasses = np.array([])
        self.samelev = samelev
        if self.comat.shape[0] != self.comat.shape[1]:
            self.samelev = False
        self.betas = betas
        self.val = 0.0
        self.currval = ''
        self.cme = np.nan
        self.eme = np.nan
        self.stc = np.nan
        self.enu = np.nan
        self.map = np.nan
        self.con = np.nan
        self.idm = np.nan
        self.cor = np.nan
        self.prl = np.nan
        self.erl = np.nan
        self.rla = np.nan
        self.hom = np.nan
        self.clt = np.nan
        self.mfu = np.nan
        self.mfs = np.nan
        self.mfsspec = np.array([])
        if np.sum(self.comat) != 1.0:
            self.comat = np.float_(self.comat) / np.sum(self.comat)
        self.calc_measure(self.measure)

    def calc_measure(self, measure='Statistical Complexity', coordmom=0, probmom=0, rllen=0, clusmom=0, samelev=True):
        """Calculates the appropriate texture measure and puts the value in the class variable val and
        updates the class variable currval with the passed string

        For a discussion of Haralick co-occurrence style texture measures see:
        R. M. Haralick, 'Statistical and structural approaches to texture'. Proceedings of the IEEE May 1979, 67(5).
        786-804.

        Parameters
        ----------

        measure: string
            One of the following measure methods (default = 'Statistical Complexity'):

                 - 'CM Entropy'
                 - 'EM Entropy'
                 - 'Statistical Complexity'
                 - 'Energy Uniformity'
                 - 'Maximum Probability'
                 - 'Contrast'
                 - 'Inverse Difference Moment'
                 - 'Correlation'
                 - 'Probability of Run Length'
                 - 'Epsilon Machine Run Length'
                 - 'Run Length Asymmetry'
                 - 'Homogeneity'
                 - 'Cluster Tendency'
                 - 'Multifractal Spectrum Energy Range'
                 - 'Multifractal Spectrum Entropy Range'

        """
        self.measure = measure
        if coordmom != 0:
            self.coordmom = coordmom
        elif probmom != 0:
            self.probmom = probmom
        elif rllen != 0:
            self.rllen = rllen
        elif clusmom != 0:
            self.clusmom = clusmom
        elif samelev == False:
            self.samelev = False
        elif self.measure == 'CM Entropy':
            if np.isnan(self.cme):
                self.cme = np.sum(-np.where(self.comat > 0.0, self.comat, 1.0) * np.where(self.comat > 0.0, np.log2(self.comat), 0.0))
            self.val = self.cme
            self.currval = 'CM Entropy'
        else:
            if self.measure == 'EM Entropy':
                if np.isnan(self.eme):
                    import scipy.linalg as L
                    if not self.emest:
                        self.est_em()
                    e, v = L.eig((np.nan_to_num(self.emmat)), left=True, right=False)
                    maxind = np.where(np.real(e) == np.max(np.real(e)))[0][0]
                    nodep = v[:, maxind] / sum(v[:, maxind])
                    self.eme = -np.sum(np.transpose(nodep * np.ones(self.emmat.shape)) * (self.emmat * np.nan_to_num(np.log2(self.emmat))))
                self.val = self.eme
                self.currval = 'EM Entropy'
            else:
                if self.measure == 'Statistical Complexity':
                    if np.isnan(self.stc):
                        import scipy.linalg as L
                        if not self.emest:
                            self.est_em()
                        e, v = L.eig((np.nan_to_num(self.emmat)), left=True, right=False)
                        maxind = np.where(np.real(e) == np.max(np.real(e)))[0][0]
                        nodep = v[:, maxind] / sum(v[:, maxind])
                        self.stc = -np.sum(nodep * np.log2(nodep))
                    self.val = self.stc
                    self.currval = 'Statistical Complexity'
                else:
                    if self.measure == 'Energy Uniformity':
                        if np.isnan(self.enu):
                            self.enu = np.sum(np.where(self.comat > 0.0, self.comat * self.comat, 0.0))
                        self.val = self.enu
                        self.currval = 'Energy Uniformity'
                    else:
                        if self.measure == 'Maximum Probability':
                            if self.map is np.nan:
                                self.map = np.max(self.comat)
                            self.val = self.map
                            self.currval = 'Maximum Probability'
                        else:
                            if self.measure == 'Contrast':
                                if not np.isnan(self.con) or self.coordmom == 0 or self.probmom == 0:
                                    if self.coordmom == 0:
                                        print('Nonzero coordinate moment is required for calculating Contrast')
                                    if self.probmom == 0:
                                        print('Nonzero probability moment is required for calculating Contrast')
                                    else:
                                        crows = np.zeros(self.comat.shape)
                                        ccols = np.zeros(self.comat.shape)
                                        for i in range(self.comat.shape[0]):
                                            crows[i, :] = i
                                            ccols[:, i] = i

                                        self.con = np.sum(np.abs(crows - ccols) ** self.coordmom * self.comat ** self.probmom)
                                self.val = self.con
                                self.currval = 'Contrast'
                            else:
                                if self.measure == 'Inverse Difference Moment':
                                    if not np.isnan(self.idm) or self.coordmom == 0 or self.probmom == 0:
                                        if self.coordmom == 0:
                                            print('Nonzero coordinate moment is required for calculating Inverse Difference Moment')
                                        if self.probmom == 0:
                                            print('Nonzero probability moment is required for calculating Inverse Difference Moment')
                                        else:
                                            crows = np.zeros(self.comat.shape)
                                            ccols = np.zeros(self.comat.shape)
                                            for i in range(self.comat.shape[0]):
                                                crows[i, :] = i
                                                ccols[:, i] = i

                                            codiffs = np.abs(crows - ccols) ** self.coordmom
                                            codiff_eps = 1e-07
                                            codiffs_ok = np.where(codiffs > codiff_eps, codiffs, 1.0)
                                            self.idm = np.sum(np.where(codiffs > codiff_eps, self.comat ** self.probmom / codiffs_ok, 0.0))
                                    self.val = self.idm
                                    self.currval = 'Inverse Difference Moment'
                                else:
                                    if self.measure == 'Correlation':
                                        if np.isnan(self.cor):
                                            import scipy.stats as ss
                                            crows = np.zeros(self.comat.shape)
                                            ccols = np.zeros(self.comat.shape)
                                            for i in range(self.comat.shape[0]):
                                                crows[i, :] = i + 1
                                                ccols[:, i] = i + 1

                                            rowmom = np.sum(crows * self.comat)
                                            colmom = np.sum(ccols * self.comat)
                                            comatvar = np.var(np.ravel(self.comat * crows))
                                            self.cor = np.sum((crows - rowmom) * (ccols - colmom) * self.comat) / comatvar
                                        self.val = self.cor
                                        self.currval = 'Correlation'
                                    else:
                                        if self.measure == 'Probability of Run Length':
                                            if np.isnan(self.prl):
                                                if self.rllen == 0:
                                                    print('Nonzero run length is required for calculating Probability of Run Length')
                                                else:
                                                    colprobs = np.zeros(self.comat.shape[0])
                                                    for i in range(self.comat.shape[0]):
                                                        colprobs[i] = np.sum(self.comat[i, :])

                                                    self.prl = 0.0
                                                    for i in range(self.comat.shape[0]):
                                                        if colprobs[i] != 0.0:
                                                            self.prl += (colprobs[i] - self.comat[(i, i)]) ** 2 * self.comat[(i, i)] ** (self.rllen - 1) / colprobs[i] ** self.rllen

                                            self.val = self.prl
                                            self.currval = 'Probability of Run Length'
                                        else:
                                            if self.measure == 'Epsilon Machine Run Length':
                                                if np.isnan(self.erl):
                                                    if self.rllen == 0:
                                                        print('Nonzero run length is required for calculating Epsilon Machine Run Length')
                                                    else:
                                                        if not self.emest:
                                                            self.est_em()
                                                        self.erl = 0.0
                                                        colprobs = np.zeros(self.emmat.shape[0])
                                                        for i in range(self.emmat.shape[0]):
                                                            colprobs[i] = np.sum(self.emmat[i, :])

                                                        for i in range(self.emmat.shape[0]):
                                                            self.erl += (colprobs[i] - self.emmat[(i, i)]) ** 2 * self.emmat[(i, i)] ** (self.rllen - 1) / colprobs[i] ** self.rllen

                                                self.val = self.erl
                                                self.currval = 'Epsilon Machine Run Length'
                                            else:
                                                if self.measure == 'Run Length Asymmetry':
                                                    if np.isnan(self.rla):
                                                        if self.rllen == 0:
                                                            print('Nonzero run length is required for calculating Run Length Asymmetry')
                                                        else:
                                                            colprobs = np.zeros(self.comat.shape[0])
                                                            rowprobs = np.zeros(self.comat.shape[0])
                                                            for i in range(self.comat.shape[0]):
                                                                colprobs[i] = np.sum(self.comat[i, :])
                                                                rowprobs[i] = np.sum(self.comat[:, i])

                                                            colval = 0.0
                                                            rowval = 0.0
                                                            for i in range(self.comat.shape[0]):
                                                                if colprobs[i] != 0.0:
                                                                    colval += (colprobs[i] - self.comat[(i, i)]) ** 2 * self.comat[(i, i)] ** (self.rllen - 1) / colprobs[i] ** self.rllen
                                                                if rowprobs[i] != 0.0:
                                                                    rowval += (rowprobs[i] - self.comat[(i, i)]) ** 2 * self.comat[(i, i)] ** (self.rllen - 1) / rowprobs[i] ** self.rllen

                                                            self.rla = np.abs(colval - rowval)
                                                    self.val = self.rla
                                                    self.currval = 'Run Length Asymmetry'
                                                else:
                                                    if self.measure == 'Homogeneity':
                                                        if np.isnan(self.hom):
                                                            crows = np.zeros(self.comat.shape)
                                                            ccols = np.zeros(self.comat.shape)
                                                            for i in range(self.comat.shape[0]):
                                                                crows[i, :] = i
                                                                ccols[:, i] = i

                                                            self.hom = np.sum(self.comat / (1 + np.abs(crows - ccols)))
                                                        self.val = self.hom
                                                        self.currval = 'Homogeneity'
                                                    else:
                                                        if self.measure == 'Cluster Tendency':
                                                            if np.isnan(self.clt):
                                                                if self.clusmom == 0:
                                                                    print('Nonzero cluster moment is required for calculating Cluster Tendency')
                                                                else:
                                                                    crows = np.zeros(self.comat.shape)
                                                                    ccols = np.zeros(self.comat.shape)
                                                                    for i in range(self.comat.shape[0]):
                                                                        crows[i, :] = i + 1
                                                                        ccols[:, i] = i + 1

                                                                    rowmom = np.sum(crows * self.comat)
                                                                    colmom = np.sum(ccols * self.comat)
                                                                    self.clt = np.sum((crows + ccols - rowmom - colmom) ** self.clusmom * self.comat)
                                                            self.val = self.clt
                                                            self.currval = 'Cluster Tendency'
                                                        else:
                                                            if self.measure == 'Multifractal Spectrum Energy Range':
                                                                if not self.emest:
                                                                    self.est_em()
                                                                else:
                                                                    if not self.mfsest:
                                                                        self.est_multi_frac_spec()
                                                                    if self.mfsspec.size != 0:
                                                                        self.mfu = np.max(self.mfsspec[:, 0]) - np.min(self.mfsspec[:, 0])
                                                                    else:
                                                                        self.mfu = 0.0
                                                                self.val = self.mfu
                                                                self.currval = 'Multifractal Spectrum Energy Range'
                                                            else:
                                                                if self.measure == 'Multifractal Spectrum Entropy Range':
                                                                    if not self.emest:
                                                                        self.est_em()
                                                                    else:
                                                                        if not self.mfsest:
                                                                            self.est_multi_frac_spec()
                                                                        if self.mfsspec.size != 0:
                                                                            self.mfs = np.max(self.mfsspec[:, 1]) - np.min(self.mfsspec[:, 1])
                                                                        else:
                                                                            self.mfs = 0.0
                                                                    self.val = self.mfs
                                                                    self.currval = 'Multifractal Spectrum Entropy Range'
                                                                else:
                                                                    (
                                                                     "Sorry don't know about texture measure ", self.measure)

    def est_multi_frac_spec(self):
        """TODO"""
        import scipy.linalg as L
        self.mfsspec = []
        if not self.emest:
            self.est_em()
        elif self.betas[2] == 1:
            print('Only 1 step asked for re. calculating multifractal spectrum, using lower limit specified, i.e. betas[0]')
            step = 0
        else:
            step = (np.float(self.betas[1]) - np.float(self.betas[0])) / (np.float(self.betas[2]) - 1)
        for i in range(self.betas[2]):
            if i == 0:
                cb = np.float(self.betas[0])
            else:
                cb = np.float(self.betas[0] + i * step)
            if cb == 1.0:
                e, v = L.eig((np.nan_to_num(self.emmat)), left=True, right=False)
                maxind = np.where(np.real(e) == np.max(np.real(e)))[0][0]
                nodep = v[:, maxind] / sum(v[:, maxind])
                su = -np.sum(np.transpose(nodep * np.ones(self.emmat.shape)) * (self.emmat * np.nan_to_num(np.log2(self.emmat))))
                self.mfsspec.append([su, su])
            elif cb == 0.0:
                splat = 0
            else:
                a = np.where(self.emmat > 0.0, np.exp(cb * np.log(self.emmat)), 0.0)
                eb, vb = L.eig((np.nan_to_num(a)), left=False, right=True)
                maxind = np.where(np.real(eb) == np.max(np.real(eb)))[0][0]
                fe = np.log2(np.real(eb[maxind]))
                b = np.dot(1 / eb[maxind] * np.diag(1 / vb[:, maxind]), np.dot(a, np.diag(vb[:, maxind])))
                e, v = L.eig((np.nan_to_num(b)), left=True, right=False)
                maxind = np.where(np.real(e) == np.max(np.real(e)))[0][0]
                nodep = v[:, maxind] / sum(v[:, maxind])
                su = abs(-np.sum(np.transpose(nodep * np.ones(b.shape)) * (b * np.nan_to_num(np.log2(b)))))
                u = abs((su - fe) / cb)
                self.mfsspec.append([u, su])

        self.mfsspec = np.array(np.real(self.mfsspec))
        self.mfsspec = np.delete(self.mfsspec, np.where(np.isnan(self.mfsspec))[0], 0)
        self.mfsest = True

    def est_em(self):
        """Estimate an epsilon machine from a co-occurrence matrix with #rows = #cols, done implicitly whenever one
        of the related complexity/entropy measures (EM Entropy, Statistical Complexity, Epsilon Machine Run Length)
        are calculated.

        For info on epsilon machines and the related measures see:

            - K. Young, Y. Chen, J. Kornak, G. B. Matson, N. Schuff, 'Summarizing complexity in high dimensions',             Phys Rev Lett. (2005) Mar 11;94(9):098701.

            - C. R. Shalizi and J. P. Crutchfield, 'Computational Mechanics: Pattern and Prediction, Structure and             Simplicity', Journal of Statistical Physics 104 (2001) 819--881.

            - K. Young and J. P. Crutchfield, 'Fluctuation Spectroscopy', Chaos, Solitons, and Fractals 4 (1993) 5-39.

            - J. P. Crutchfield and K. Young, 'Computation at the Onset of Chaos', in Entropy, Complexity, and Physics             of Information, W. Zurek, editor, SFI Studies in the Sciences of Complexity, VIII, Addison-Wesley, Reading,            Massachusetts (1990) 223-269.

            - C. R. Shalizi and J. P. Crutchfield, 'Computational Mechanics: Pattern and Prediction, Structure and             Simplicity', Journal of Statistical Physics 104 (2001) 819--881.
        """
        import scipy.stats as ss
        self.condo = np.transpose(np.transpose(self.comat) / np.sum((self.comat), axis=1))
        found = []
        self.emclasses = np.zeros(self.condo.shape[0], int)
        onclass = 0
        for i in range(self.condo.shape[0]):
            if i not in found:
                found.append(i)
                if np.sum(self.condo[i, :]) < 1e-08:
                    self.emclasses[i] = 0
                else:
                    self.emclasses[i] = onclass
                    for j in range(i + 1, self.condo.shape[0]):
                        if j not in found:
                            tester = ss.chisquare(self.totcount * self.condo[i, :], self.totcount * self.condo[j, :])[1]
                            if tester < self.clusp:
                                found.append(j)
                                onclass += 1
                                self.emclasses[j] = onclass
                            else:
                                found.append(j)
                                self.emclasses[j] = onclass

        self.emclus = onclass + 1
        for i in range(self.emclus):
            rowinds = tuple(np.where(self.emclasses == i)[0])
            if i == 0:
                a = np.add.reduce((self.comat[rowinds, :]), axis=0)
            else:
                a = np.vstack((a, np.add.reduce((self.comat[rowinds, :]), axis=0)))

        if self.samelev:
            if len(a.shape) > 1:
                for i in range(self.emclus):
                    colinds = tuple(np.where(self.emclasses == i)[0])
                    if i == 0:
                        b = np.add.reduce((a[:, colinds]), axis=1)
                    else:
                        b = np.vstack((b, np.add.reduce((a[:, colinds]), axis=1)))

            else:
                for i in range(a.shape[0]):
                    if i == 0:
                        b = a
                    else:
                        b = np.vstack([b, a])

            self.emmat = np.transpose(b)
        else:
            found = []
            self.emclasses = np.zeros(self.condo.shape[1], int)
            onclass = 0
            for i in range(self.condo.shape[1]):
                if i not in found:
                    found.append(i)
                    if np.sum(self.condo[:, i]) < 1e-08:
                        self.emclasses[i] = 0
                    else:
                        self.emclasses[i] = onclass
                        for j in range(self.condo.shape[1], i + 1):
                            if j not in found:
                                tester = ss.chisquare(self.totcount * self.condo[:, i], self.totcount * self.condo[:, j])[1]
                                if tester < self.clusp:
                                    found.append(j)
                                    onclass += 1
                                    self.emclasses[j] = onclass
                                else:
                                    found.append(j)
                                    self.emclasses[j] = onclass

            self.emclus = onclass + 1
            for i in range(self.emclus):
                colinds = tuple(np.where(self.emclasses == i)[1])
                if i == 0:
                    a = np.add.reduce((self.comat[:, colinds]), axis=1)
                else:
                    a = np.vstack((a, np.add.reduce((self.comat[:, colinds]), axis=1)))

            self.emmat = np.transpose(a)
        self.emmat = np.transpose(np.transpose(self.emmat) / np.sum((self.emmat), axis=1))
        self.emest = True