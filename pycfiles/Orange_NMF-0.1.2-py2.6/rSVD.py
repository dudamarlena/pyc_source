# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/_nmf/widgets/rSVD.py
# Compiled at: 2012-08-30 09:54:04
"""
@author: Fajwel
"""
import numpy as np

class rSVD:

    def __init__(self):
        self.aa = 0

    def isMissing(self, X):
        return X == -99999999

    def rank(self, x):
        isMis = self.isMissing(x)
        isNotMis = np.logical_not(isMis)
        nbMis = sum(isMis)
        x[isMis] = max(x[isNotMis])
        xSorted = np.argsort(x)
        return xSorted[0:len(x) - nbMis]

    def doRSVD(self, M0, nTrial, MaxIter, StdGlobLoc, LTScov, ncUser, StepIter, MaxNonImpr, tolerance):
        missVal = -99999999
        n = M0.shape[0]
        p = M0.shape[1]
        if StdGlobLoc >= 2:
            npcov = np.round(n * p * LTScov)
            ncov = np.round(n * LTScov)
            pcov = np.round(p * LTScov)
            nptrim = n * p - npcov
        else:
            nptrim = 0
        if not nptrim:
            StdGlobLoc = 1
        nc = min(n, p, ncUser)
        Mev = np.zeros(nc)
        if StdGlobLoc > 1:
            MaxTrial = nTrial
        else:
            MaxTrial = 1
        M0init = M0.copy()
        Mw = np.zeros([p, nc])
        Mt = np.zeros([n, nc])
        w = np.zeros(p)
        t = np.zeros(n)
        if not np.any(self.isMissing(M0)) and StdGlobLoc == 1:
            FastCode = 1
        else:
            FastCode = 0
        j1 = 0
        j2 = p
        self.t = []
        MMis0 = self.isMissing(M0)
        for k in range(0, nc):
            for iTrial in range(1, MaxTrial + 1):
                M = M0.copy()
                if StdGlobLoc > 1:
                    M = M.reshape(n * p)
                    M[np.random.permutation(n * p)[npcov:n * p]] = missVal
                    M = M.reshape((n, p))
                MMis = self.isMissing(M)
                for j in range(0, p):
                    w[j] = np.median(M[:, j][(M[:, j] != missVal)])

                if not sum(w > 0):
                    w = np.ones(p)
                w = w / np.sqrt(np.dot(w, w))
                if not FastCode:
                    for i in range(0, n):
                        cells = np.logical_not(MMis[i, :])
                        if sum(cells) > 1:
                            t[i] = np.dot(M[(i, cells)], w[cells]) / np.dot(w[cells], w[cells])
                        else:
                            t[i] = missVal

                else:
                    t = np.dot(M, w) / np.dot(w, w)
                self.t.append(t)
                t[self.isMissing(t)] = np.median(t[(t != missVal)])
                if StdGlobLoc >= 2:
                    Mdiff = abs(M0 - np.dot(np.array([t]).T, np.array([w])))
                    Mdiff[MMis0] = missVal
                    RMdiff = self.rank(np.reshape(Mdiff, n * p))
                    cells = RMdiff[0:min(npcov, len(RMdiff))]
                    M = missVal * np.ones(n * p)
                    M[cells] = M0.reshape(n * p)[cells]
                    M = M.reshape((n, p))
                    MMis = self.isMissing(M)
                iteration = 0
                cont = 1
                while cont and iteration < MaxIter:
                    if not FastCode:
                        for j in range(0, p):
                            cells = np.logical_not(MMis[:, j])
                            if iteration >= 0 and StdGlobLoc == 3:
                                if sum(cells) < ncov:
                                    RMdiff = self.rank(Mdiff[:, j])
                                    cells = RMdiff[0:min(ncov, len(RMdiff))]
                                    M[(cells, j)] = M0[(cells, j)]
                            if sum(cells) > 1:
                                w[j] = np.dot(t[cells], M[(cells, j)]) / np.dot(t[cells], t[cells])
                            else:
                                w[j] = missVal

                    else:
                        w = np.dot(M.T, t) / np.dot(t, t)
                    w[self.isMissing(w)] = np.median(w[(w != missVal)])
                    w = w / np.sqrt(np.dot(w, w))
                    if StdGlobLoc >= 2:
                        Mdiff = abs(M0 - np.dot(np.array([t]).T, np.array([w])))
                        Mdiff[MMis0] = missVal
                        RMdiff = self.rank(np.reshape(Mdiff, n * p))
                        cells = RMdiff[0:min(npcov, len(RMdiff))]
                        M = missVal * np.ones(n * p)
                        M[cells] = M0.reshape(n * p)[cells]
                        M = M.reshape((n, p))
                        MMis = self.isMissing(M)
                    if not FastCode:
                        for i in range(0, n):
                            cells = np.logical_not(MMis)[i, j1:j2]
                            if iteration >= 0 and StdGlobLoc == 3:
                                if sum(cells) < pcov:
                                    RMdiff = self.rank(Mdiff[i, j1:j2])
                                    cells = RMdiff[0:min(pcov, len(RMdiff))]
                                    M[(i, cells)] = M0[(i, cells)]
                            if sum(cells) > 1:
                                t[i] = np.dot(M[(i, cells)], w[cells]) / np.dot(w[cells], w[cells])
                            else:
                                t[i] = missVal

                    else:
                        t = np.dot(M, w) / np.dot(w, w)
                    t[self.isMissing(t)] = np.median(t[(t != missVal)])
                    if StdGlobLoc >= 2:
                        Mdiff = abs(M0 - np.dot(np.array([t]).T, np.array([w])))
                        Mdiff[MMis0] = missVal
                        RMdiff = self.rank(np.reshape(Mdiff, n * p))
                        cells = RMdiff[0:min(npcov, len(RMdiff))]
                        M = missVal * np.ones(n * p)
                        M[cells] = M0.reshape(n * p)[cells]
                        M = M.reshape((n, p))
                        MMis = self.isMissing(M)
                    if np.mod(iteration, StepIter) == 0:
                        if StdGlobLoc == 1:
                            Mdiff = abs(M0 - np.dot(np.array([t]).T, np.array([w])))
                            Mdiff[MMis0] = missVal
                        cells = np.logical_not(MMis)
                        Vdiff = Mdiff[cells]
                        diff = np.dot(Vdiff, Vdiff) / sum(sum(cells))
                        if iteration == 0:
                            BackDiff = diff
                            BackMw = w
                            BackMt = t
                            NonImpr = 0
                        elif abs(diff - diff0) / diff0 < tolerance:
                            cont = 0
                        elif diff > BackDiff:
                            NonImpr += 1
                            if NonImpr > MaxNonImpr and MaxNonImpr:
                                cont = 0
                        elif diff <= BackDiff:
                            BackDiff = diff
                            BackMw = w
                            BackMt = t
                            NonImpr = 0
                        diff0 = diff
                    iteration += 1

                diff = BackDiff
                w = BackMw
                t = BackMt
                if iTrial == 1 or diff < DiffTrial:
                    DiffTrial = diff
                    tTrial = t.copy()
                    wTrial = w.copy()

            t = tTrial
            w = wTrial
            Mw[:, k] = w
            if StdGlobLoc > 1:
                t = t / np.sqrt(np.dot(t, t))
                Mt[:, k] = t
                RMdiff = self.rank(np.reshape(Mdiff, n * p))
                Ycells = M0.reshape(n * p)[RMdiff][0:min(npcov, len(RMdiff))]
                Xcells = np.reshape(np.dot(np.array([t]).T, np.array([w])), n * p)[RMdiff][0:min(npcov, len(RMdiff))]
                Mev[k] = np.dot(Ycells, Xcells) / np.dot(Xcells, Xcells)
            else:
                Mev[k] = np.sqrt(np.dot(t, t))
                Mt[:, k] = t / Mev[k]
            M0 = M0 - Mev[k] * np.dot(np.array([Mt[:, k]]).T, np.array([Mw[:, k]]))
            M0[MMis0] = missVal

        if nc > 1:
            RMev = np.argsort(-Mev)
            Mev = Mev[RMev]
            Mw0 = Mw.copy()
            Mt0 = Mt.copy()
            for k in range(0, nc):
                Mw[:, k] = Mw0[:, RMev[k]]
                Mt[:, k] = Mt0[:, RMev[k]]

        M0 = M0init
        self.U = Mt
        self.V = Mw
        self.D = Mev