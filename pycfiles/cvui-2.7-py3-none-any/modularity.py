# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cvu/modularity.py
# Compiled at: 2013-03-14 11:55:23
import numpy as np, scipy.linalg as lin

def threshold_prop(adjmat, threshold_p, delete_extras=False):
    adjmat = np.triu(adjmat)
    asort = np.sort(adjmat.ravel())
    cutoff = asort[int((1 - threshold_p / 2) * len(asort))]
    adjmat[adjmat < cutoff] = 0
    adjmat = adjmat + adjmat.transpose()
    if delete_extras:
        deleters = np.nonzero(np.sum(adjmat, axis=1) == 0)[0]
        adjmat = np.delete(adjmat, deleters, axis=0)
        adjmat = np.delete(adjmat, deleters, axis=1)
        print '%i nodes were deleted from the graph due to null connections' % len(deleters)
    else:
        deleters = np.array(())
    return (
     adjmat, deleters)


def comm2list(indices, zeroindexed=False):
    nr_indices = max(indices)
    ls = []
    for c in xrange(0, nr_indices, 1):
        ls.append([])

    i = 0
    z = int(not zeroindexed)
    for i in xrange(0, len(indices), 1):
        ls[(indices[i] - z)].append(i)

    return ls


def list2comm(mlist, zeroindexed=False):
    nr_indices = sum(map(len, mlist))
    ci = np.zeros((nr_indices,))
    z = int(not zeroindexed)
    for i in xrange(0, len(mlist), 1):
        for j in xrange(0, len(mlist[i]), 1):
            ci[mlist[i][j]] = i + z

    return list(ci)


def unpermute(mods, perm, forward=False):
    mapper = {}
    for i in xrange(0, len(perm), 1):
        if forward:
            mapper.update({i: perm[i]})
        else:
            mapper.update({perm[i]: i})

    new_mods = []
    for mod in mods:
        new_mods.append(map(mapper.get, mod))

    if forward:
        new_mods.remove
    return new_mods


def reacquire_olds(deleters, nr_nodes):
    olds = range(0, nr_nodes, 1)
    c = 0
    for i in xrange(0, nr_nodes + len(deleters), 1):
        if i in deleters:
            c += 1
        else:
            olds[(i - c)] += c

    return olds


def use_metis(adjmat, threshold_p=0.3, nr_modules=8):
    import networkx as nx, metis
    adjmat, deleters = threshold_prop(adjmat, threshold_p)
    g = nx.Graph(adjmat)
    objval, parts = metis.part_graph(g, nr_modules)
    ret = []
    for i in xrange(0, nr_modules, 1):
        ret.append(np.array(np.nonzero(np.array(parts) == i)))

    return ret
    if len(deleters) == 0:
        return ret
    else:
        reinsert_olds_perm = reacquire_olds(deleters, len(adjmat))
        modules = unpermute(ret, reinsert_olds_perm, forward=True)
        return modules


def spectral_partition(adjmat, delete_extras=False, threshold_p=0.3):
    adjmat, deleters = threshold_prop(adjmat, threshold_p, delete_extras=delete_extras)
    nr_nodes = len(adjmat)
    permutation = np.array(range(0, nr_nodes, 1))
    k = np.sum(adjmat, axis=0)
    m = np.sum(k)
    init_modmat = adjmat - np.outer(k, k) / (1.0 * m)
    modules = []

    def recur(module, modmat):
        n = len(modmat)
        d, v = lin.eigh(modmat)
        i = np.nonzero(d == np.max(d))[0]
        max_eigvec = v[:, i]
        mod_asgn = (max_eigvec >= 0) * 2 - 1
        q = np.dot(mod_asgn.T, np.dot(modmat, mod_asgn))[0][0]
        if q > 0:
            qmax = q
            modmat = modmat - np.diag(np.diag(modmat))
            it = np.ma.masked_array(np.ones((n, 1)), False)
            mod_asgn_iter = mod_asgn.copy()
            itr_num = 0
            while np.any(it):
                q_iter = qmax - 4 * mod_asgn_iter * np.dot(modmat, mod_asgn_iter)
                qmax = np.max(q_iter * it)
                imax = np.nonzero(q_iter == qmax)
                mod_asgn_iter[imax] *= -1
                it[imax] = np.ma.masked
                if qmax > q:
                    q = qmax
                    mod_asgn = mod_asgn_iter
                itr_num += 1
                if itr_num > 2 * n:
                    raise Exception('DIEDIEDIE')

            if np.abs(np.sum(mod_asgn)) == n:
                modules.append(np.array(module).tolist())
                return
            mod1 = module[np.nonzero(mod_asgn == 1)[0]]
            mod2 = module[np.nonzero(mod_asgn == -1)[0]]
            modmat1 = init_modmat[mod1][:, mod1]
            modmat1 -= np.diag(np.sum(modmat1, axis=0))
            modmat2 = init_modmat[mod2][:, mod2]
            modmat2 -= np.diag(np.sum(modmat2, axis=0))
            recur(mod1, modmat1)
            recur(mod2, modmat2)
            return
        else:
            modules.append(np.array(module).tolist())
            return

    recur(permutation, init_modmat.copy())
    if len(deleters) == 0:
        return modules
    else:
        reinsert_olds_perm = reacquire_olds(deleters, nr_nodes)
        modules = unpermute(modules, reinsert_olds_perm, forward=True)
        return modules


class NaiveSpectralPartitioner:

    def __init__(self, adjmat, nr_edges=0):
        self.adjmat = adjmat
        self.nr_nodes = len(self.adjmat)

    def partition(self):
        self.adjmat = threshold_prop(self.adjmat)
        adj = self.adjmat
        nr_edges = len(np.nonzero(adj)[1])
        degvec = np.zeros([len(adj), 1])
        for i in xrange(0, len(adj), 1):
            degvec[i] = int(len(np.transpose(np.nonzero(adj[i, :]))))

        degmat = np.zeros([len(adj), len(adj)])
        for i in xrange(0, len(self.adjmat), 1):
            for j in xrange(0, len(adj), 1):
                degmat[(i, j)] = degvec[i] * degvec[j]

        self.modmat = adj - degmat / (2 * nr_edges)
        startgrp = np.arange(self.nr_nodes, dtype=int).T
        self.ret_modules = []
        self.recur_partition(self.modmat, startgrp, startgrp.copy())
        return self.ret_modules

    def recur_partition(self, modmat, curgrp, curgrpinds):
        adjusted_modmat = modmat.copy()
        adjusted_modmat -= np.diag(np.diag(np.sum(modmat, axis=0)))
        print np.diag(adjusted_modmat)
        print np.diag(modmat)
        print adjusted_modmat[:, 0]
        grp1, grp2, eigvec = self.bipartition(adjusted_modmat, len(curgrp))
        print np.shape(grp1)
        print np.shape(grp2)
        print np.shape(eigvec)
        print eigvec
        dq = np.dot(np.dot(eigvec.T, adjusted_modmat), eigvec)
        print dq
        if dq > 0 and not len(curgrp) <= 7:
            modmat_grp1 = np.delete(modmat, grp2, axis=0)
            modmat_grp1 = np.delete(modmat_grp1, grp2, axis=1)
            print 'grp1 modmat' + str(np.shape(modmat_grp1))
            self.recur_partition(modmat_grp1, grp1, curgrpinds[grp1])
            modmat_grp2 = np.delete(modmat, grp1, axis=0)
            modmat_grp2 = np.delete(modmat_grp2, grp1, axis=1)
            print 'grp2 modmat' + str(np.shape(modmat_grp2))
            self.recur_partition(modmat_grp2, grp2, curgrpinds[grp2])
        else:
            print curgrp.T
            print np.shape(curgrp)
            self.ret_modules.append(curgrpinds.T)

    def bipartition(self, modmat, nr_nodes):
        if nr_nodes == 0:
            return
        d, v = lin.eig(modmat)
        lambdamax = np.max(d)
        c = np.nonzero(d == lambdamax)
        eigvec = np.reshape(v[:, c], (nr_nodes,))
        classify = np.sign(eigvec)
        classify[classify == 0] = -1
        grp1 = np.nonzero(classify == 1)
        grp2 = np.nonzero(classify == -1)
        grp1 = np.array(grp1)
        grp1 = grp1.T
        grp2 = np.array(grp2)
        grp2 = grp2.T
        return (grp1, grp2, classify)