# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/aestrivex/anaconda3/lib/python3.7/site-packages/bct/algorithms/modularity.py
# Compiled at: 2020-04-27 14:47:22
# Size of source mod 2**32: 60824 bytes
from __future__ import division, print_function
import numpy as np
from bct.utils import BCTParamError, normalize, get_rng
from ..due import BibTeX, due
from ..citations import LEICHT2008, REICHARDT2006, GOOD2010, SUN2008, RUBINOV2011, BLONDEL2008, MEILA2007

def ci2ls(ci):
    """
    Convert from a community index vector to a 2D python list of modules
    The list is a pure python list, not requiring numpy.

    Parameters
    ----------
    ci : Nx1 np.ndarray
        the community index vector
    zeroindexed : bool
        If True, ci uses zero-indexing (lowest value is 0). Defaults to False.

    Returns
    -------
    ls : listof(list)
        pure python list with lowest value zero-indexed
        (regardless of zero-indexing parameter)
    """
    if not np.size(ci):
        return ci
    _, ci = np.unique(ci, return_inverse=True)
    ci += 1
    nr_indices = int(max(ci))
    ls = []
    for c in range(nr_indices):
        ls.append([])

    for i, x in enumerate(ci):
        ls[(ci[i] - 1)].append(i)

    return ls


def ls2ci(ls, zeroindexed=False):
    """
    Convert from a 2D python list of modules to a community index vector.
    The list is a pure python list, not requiring numpy.

    Parameters
    ----------
    ls : listof(list)
        pure python list with lowest value zero-indexed
        (regardless of value of zeroindexed parameter)
    zeroindexed : bool
        If True, ci uses zero-indexing (lowest value is 0). Defaults to False.

    Returns
    -------
    ci : Nx1 np.ndarray
        community index vector
    """
    if ls is None or np.size(ls) == 0:
        return ()
    nr_indices = sum(map(len, ls))
    ci = np.zeros((nr_indices,), dtype=int)
    z = int(not zeroindexed)
    for i, x in enumerate(ls):
        for j, y in enumerate(ls[i]):
            ci[ls[i][j]] = i + z

    return ci


def community_louvain(W, gamma=1, ci=None, B='modularity', seed=None):
    """
    The optimal community structure is a subdivision of the network into
    nonoverlapping groups of nodes which maximizes the number of within-group
    edges and minimizes the number of between-group edges.

    This function is a fast an accurate multi-iterative generalization of the
    louvain community detection algorithm. This function subsumes and improves
    upon modularity_[louvain,finetune]_[und,dir]() and additionally allows to
    optimize other objective functions (includes built-in Potts Model i
    Hamiltonian, allows for custom objective-function matrices).

    Parameters
    ----------
    W : NxN np.array
        directed/undirected weighted/binary adjacency matrix
    gamma : float
        resolution parameter. default value=1. Values 0 <= gamma < 1 detect
        larger modules while gamma > 1 detects smaller modules.
        ignored if an objective function matrix is specified.
    ci : Nx1 np.arraylike
        initial community affiliation vector. default value=None
    B : str | NxN np.arraylike
        string describing objective function type, or provides a custom
        NxN objective-function matrix. builtin values 
            'modularity' uses Q-metric as objective function
            'potts' uses Potts model Hamiltonian.
            'negative_sym' symmetric treatment of negative weights
            'negative_asym' asymmetric treatment of negative weights
    seed : hashable, optional
        If None (default), use the np.random's global random state to generate random numbers.
        Otherwise, use a new np.random.RandomState instance seeded with the given value.

    Returns
    -------
    ci : Nx1 np.array
        final community structure
    q : float
        optimized q-statistic (modularity only)
    """
    rng = get_rng(seed)
    n = len(W)
    s = np.sum(W)
    if ci is None:
        ci = np.arange(n) + 1
    else:
        if len(ci) != n:
            raise BCTParamError('initial ci vector size must equal N')
        _, ci = np.unique(ci, return_inverse=True)
        ci += 1
    Mb = ci.copy()
    renormalize = False
    if B in ('negative_sym', 'negative_asym'):
        renormalize = True
        W0 = W * (W > 0)
        s0 = np.sum(W0)
        B0 = W0 - gamma * np.outer(np.sum(W0, axis=1), np.sum(W0, axis=0)) / s0
        W1 = -W * (W < 0)
        s1 = np.sum(W1)
        if s1:
            B1 = W1 - gamma * np.outer(np.sum(W1, axis=1), np.sum(W1, axis=0)) / s1
        else:
            B1 = 0
    else:
        if np.min(W) < -1e-10:
            raise BCTParamError('Input connection matrix contains negative weights but objective function dealing with negative weights was not selected')
        if B == 'potts':
            if np.any(np.logical_not(np.logical_or(W == 0, W == 1))):
                raise BCTParamError('Potts hamiltonian requires binary input matrix')
    if B == 'modularity':
        B = W - gamma * np.outer(np.sum(W, axis=1), np.sum(W, axis=0)) / s
    else:
        if B == 'potts':
            B = W - gamma * np.logical_not(W)
        else:
            if B == 'negative_sym':
                B = B0 / (s0 + s1) - B1 / (s0 + s1)
            else:
                if B == 'negative_asym':
                    B = B0 / s0 - B1 / (s0 + s1)
                else:
                    try:
                        B = np.array(B)
                    except:
                        raise BCTParamError('unknown objective function type')

                    if B.shape != W.shape:
                        raise BCTParamError('objective function matrix does not match size of adjacency matrix')
                    if not np.allclose(B, B.T):
                        print('Warning: objective function matrix not symmetric, symmetrizing')
                        B = (B + B.T) / 2
                    Hnm = np.zeros((n, n))
                    for m in range(1, n + 1):
                        Hnm[:, m - 1] = np.sum((B[:, ci == m]), axis=1)

                    H = np.sum(Hnm, axis=1)
                    Hm = np.sum(Hnm, axis=0)
                    q0 = -np.inf
                    q = np.sum(B[(np.tile(ci, (n, 1)) == np.tile(ci, (n, 1)).T)]) / s
                    first_iteration = True
                    while q - q0 > 1e-10:
                        it = 0
                        flag = True
                        while flag:
                            it += 1
                            if it > 1000:
                                raise BCTParamError('Modularity infinite loop style G. Please contact the developer.')
                            flag = False
                            for u in rng.permutation(n):
                                ma = Mb[u] - 1
                                dQ = Hnm[u, :] - Hnm[(u, ma)] + B[(u, u)]
                                dQ[ma] = 0
                                max_dq = np.max(dQ)
                                if max_dq > 1e-10:
                                    flag = True
                                    mb = np.argmax(dQ)
                                    Hnm[:, mb] += B[:, u]
                                    Hnm[:, ma] -= B[:, u]
                                    Hm[mb] += H[u]
                                    Hm[ma] -= H[u]
                                    Mb[u] = mb + 1

                        _, Mb = np.unique(Mb, return_inverse=True)
                        Mb += 1
                        M0 = ci.copy()
                        if first_iteration:
                            ci = Mb.copy()
                            first_iteration = False
                        else:
                            for u in range(1, n + 1):
                                ci[M0 == u] = Mb[(u - 1)]

                        n = np.max(Mb)
                        b1 = np.zeros((n, n))
                        for i in range(1, n + 1):
                            for j in range(i, n + 1):
                                bm = np.sum(B[np.ix_(Mb == i, Mb == j)])
                                b1[(i - 1, j - 1)] = bm
                                b1[(j - 1, i - 1)] = bm

                        B = b1.copy()
                        Mb = np.arange(1, n + 1)
                        Hnm = B.copy()
                        H = np.sum(B, axis=0)
                        Hm = H.copy()
                        q0 = q
                        q = np.trace(B)

                    if not renormalize:
                        return (
                         ci, q / s)
                    return (ci, q)


def link_communities(W, type_clustering='single'):
    """
    The optimal community structure is a subdivision of the network into
    nonoverlapping groups of nodes which maximizes the number of within-group
    edges and minimizes the number of between-group edges.

    This algorithm uncovers overlapping community structure via hierarchical
    clustering of network links. This algorithm is generalized for
    weighted/directed/fully-connected networks

    Parameters
    ----------
    W : NxN np.array
        directed weighted/binary adjacency matrix
    type_clustering : str
        type of hierarchical clustering. 'single' for single-linkage,
        'complete' for complete-linkage. Default value='single'

    Returns
    -------
    M : CxN np.ndarray
        nodal community affiliation matrix.
    """
    n = len(W)
    W = normalize(W)
    if type_clustering not in ('single', 'complete'):
        raise BCTParamError('Unrecognized clustering type')
    np.fill_diagonal(W, 0)
    W[(range(n), range(n))] = (np.sum(W, axis=0) / np.sum((np.logical_not(W)), axis=0) + np.sum((W.T), axis=0) / np.sum((np.logical_not(W.T)), axis=0)) / 2
    No = np.sum((W ** 2), axis=1)
    Ni = np.sum((W ** 2), axis=0)
    Jo = np.zeros((n, n))
    Ji = np.zeros((n, n))
    for b in range(n):
        for c in range(n):
            Do = np.dot(W[b, :], W[c, :].T)
            Jo[(b, c)] = Do / (No[b] + No[c] - Do)
            Di = np.dot(W[:, b].T, W[:, c])
            Ji[(b, c)] = Di / (Ni[b] + Ni[c] - Di)

    A, B = np.where(np.logical_and(np.logical_or(W, W.T), np.triu(np.ones((n, n)), 1)))
    m = len(A)
    Ln = np.zeros((m, 2), dtype=(np.int32))
    Lw = np.zeros((m,))
    for i in range(m):
        Ln[i, :] = (A[i], B[i])
        Lw[i] = (W[(A[i], B[i])] + W[(B[i], A[i])]) / 2

    ES = np.zeros((m, m), dtype=(np.float32))
    for i in range(m):
        for j in range(m):
            if Ln[(i, 0)] == Ln[(j, 0)]:
                a = Ln[(i, 0)]
                b = Ln[(i, 1)]
                c = Ln[(j, 1)]
            else:
                if Ln[(i, 0)] == Ln[(j, 1)]:
                    a = Ln[(i, 0)]
                    b = Ln[(i, 1)]
                    c = Ln[(j, 0)]
                else:
                    if Ln[(i, 1)] == Ln[(j, 0)]:
                        a = Ln[(i, 1)]
                        b = Ln[(i, 0)]
                        c = Ln[(j, 1)]
                    else:
                        if Ln[(i, 1)] == Ln[(j, 1)]:
                            a = Ln[(i, 1)]
                            b = Ln[(i, 0)]
                            c = Ln[(j, 0)]
                        else:
                            continue
                        ES[(i, j)] = (W[(a, b)] * W[(a, c)] * Ji[(b, c)] + W[(b, a)] * W[(c, a)] * Jo[(b, c)]) / 2

    np.fill_diagonal(ES, 0)
    C = np.zeros((m, m), dtype=(np.int32))
    Nc = C.copy()
    Mc = np.zeros((m, m), dtype=(np.float32))
    Dc = Mc.copy()
    U = np.arange(m)
    C[0, :] = np.arange(m)
    import time
    for i in range(m - 1):
        print('hierarchy %i' % i)
        for j in range(len(U)):
            ixes = C[i, :] == U[j]
            links = np.sort(Lw[ixes])
            nodes = np.sort(np.reshape(Ln[ixes, :], 2 * np.size(np.where(ixes))))
            nodulo = np.append(nodes[0], nodes[1:][(nodes[1:] != nodes[:-1])])
            nc = len(nodulo)
            mc = np.sum(links)
            min_mc = np.sum(links[:nc - 1])
            dc = (mc - min_mc) / (nc * (nc - 1) / 2 - min_mc)
            if np.array(dc).shape is not ():
                print(dc)
                print(dc.shape)
            Nc[(i, j)] = nc
            Mc[(i, j)] = mc
            Dc[(i, j)] = dc if not np.isnan(dc) else 0

        C[i + 1, :] = C[i, :]
        u1, u2 = np.where(ES[np.ix_(U, U)] == np.max(ES[np.ix_(U, U)]))
        if np.size(u1) > 2:
            wehr, = np.where(u1 == u2[0])
            uc = np.squeeze((u1[0], u2[0]))
            ud = np.squeeze((u1[wehr], u2[wehr]))
            u1 = uc
            u2 = ud
        ugl = np.sort((u1, u2), axis=1)
        ug_rows = ugl[np.argsort(ugl, axis=0)[:, 0]]
        unq_rows = np.vstack({tuple(row) for row in ug_rows})
        V = U[unq_rows]
        for j in range(len(V)):
            if type_clustering == 'single':
                x = np.max((ES[V[j, :], :]), axis=0)
            else:
                if type_clustering == 'complete':
                    x = np.min((ES[V[j, :], :]), axis=0)
                ES[V[j, :], :] = np.array((x, x))
                ES[:, V[j, :]] = np.transpose((x, x))
                ES[(V[(j, 0)], V[(j, 0)])] = 0
                ES[(V[(j, 1)], V[(j, 1)])] = 0
                C[(i + 1, C[i + 1, :] == V[(j, 1)])] = V[(j, 0)]
                V[V == V[(j, 1)]] = V[(j, 0)]

        U = np.unique(C[i + 1, :])
        if len(U) == 1:
            break

    i = np.argmax(np.sum((Dc * Mc), axis=1))
    U = np.unique(C[i, :])
    M = np.zeros((len(U), n))
    for j in range(len(U)):
        M[(j, np.unique(Ln[C[i, :] == U[j], :]))] = 1

    M = M[np.sum(M, axis=1) > 2, :]
    return M


def _safe_squeeze(arr, *args, **kwargs):
    """
    numpy.squeeze will reduce a 1-item array down to a zero-dimensional "array",
    which is not necessarily desirable.
    This function does the squeeze operation, but ensures that there is at least
    1 dimension in the output.
    """
    out = (np.squeeze)(arr, *args, **kwargs)
    if np.ndim(out) == 0:
        out = out.reshape((1, ))
    return out


@due.dcite((BibTeX(LEICHT2008)), description='Directed modularity')
@due.dcite((BibTeX(REICHARDT2006)), description='Directed modularity')
@due.dcite((BibTeX(GOOD2010)), description='Directed modularity')
def modularity_dir(A, gamma=1, kci=None):
    """
    The optimal community structure is a subdivision of the network into
    nonoverlapping groups of nodes in a way that maximizes the number of
    within-group edges, and minimizes the number of between-group edges.
    The modularity is a statistic that quantifies the degree to which the
    network may be subdivided into such clearly delineated groups.

    Parameters
    ----------
    W : NxN np.ndarray
        directed weighted/binary connection matrix
    gamma : float
        resolution parameter. default value=1. Values 0 <= gamma < 1 detect
        larger modules while gamma > 1 detects smaller modules.
    kci : Nx1 np.ndarray | None
        starting community structure. If specified, calculates the Q-metric
        on the community structure giving, without doing any optimzation.
        Otherwise, if not specified, uses a spectral modularity maximization
        algorithm.

    Returns
    -------
    ci : Nx1 np.ndarray
        optimized community structure
    Q : float
        maximized modularity metric

    Notes
    -----
    This algorithm is deterministic. The matlab function bearing this
    name incorrectly disclaims that the outcome depends on heuristics
    involving a random seed. The louvain method does depend on a random seed,
    but this function uses a deterministic modularity maximization algorithm.
    """
    from scipy import linalg
    n = len(A)
    ki = np.sum(A, axis=0)
    ko = np.sum(A, axis=1)
    m = np.sum(ki)
    b = A - gamma * np.outer(ko, ki) / m
    B = b + b.T
    init_mod = np.arange(n)
    modules = []

    def recur(module):
        n = len(module)
        modmat = B[module][:, module]
        vals, vecs = linalg.eig(modmat)
        rlvals = np.real(vals)
        max_eigvec = _safe_squeeze(vecs[:, np.where(rlvals == np.max(rlvals))])
        if max_eigvec.ndim > 1:
            max_eigvec = max_eigvec[:, 0]
        else:
            mod_asgn = _safe_squeeze((max_eigvec >= 0) * 2 - 1)
            q = np.dot(mod_asgn, np.dot(modmat, mod_asgn))
            if q > 0:
                qmax = q
                np.fill_diagonal(modmat, 0)
                it = np.ma.masked_array(np.ones((n,)), False)
                mod_asgn_iter = mod_asgn.copy()
                while np.any(it):
                    q_iter = qmax - 4 * mod_asgn_iter * np.dot(modmat, mod_asgn_iter)
                    qmax = np.max(q_iter * it)
                    imax = np.argmax(q_iter * it)
                    mod_asgn_iter[imax] *= -1
                    it[imax] = np.ma.masked
                    if qmax > q:
                        q = qmax
                        mod_asgn = mod_asgn_iter

                if np.abs(np.sum(mod_asgn)) == n:
                    modules.append(np.array(module).tolist())
                else:
                    mod1 = module[np.where(mod_asgn == 1)]
                    mod2 = module[np.where(mod_asgn == -1)]
                    recur(mod1)
                    recur(mod2)
            else:
                modules.append(np.array(module).tolist())

    if kci is None:
        recur(init_mod)
        ci = ls2ci(modules)
    else:
        ci = kci
    s = np.tile(ci, (n, 1))
    q = np.sum(np.logical_not(s - s.T) * B / (2 * m))
    return (ci, q)


@due.dcite((BibTeX(SUN2008)), description='Finetuned directed modularity')
@due.dcite((BibTeX(RUBINOV2011)), description='Finetuned directed modularity')
def modularity_finetune_dir(W, ci=None, gamma=1, seed=None):
    """
    The optimal community structure is a subdivision of the network into
    nonoverlapping groups of nodes in a way that maximizes the number of
    within-group edges, and minimizes the number of between-group edges.
    The modularity is a statistic that quantifies the degree to which the
    network may be subdivided into such clearly delineated groups.

    This algorithm is inspired by the Kernighan-Lin fine-tuning algorithm
    and is designed to refine a previously detected community structure.

    Parameters
    ----------
    W : NxN np.ndarray
        directed weighted/binary connection matrix
    ci : Nx1 np.ndarray | None
        initial community affiliation vector
    gamma : float
        resolution parameter. default value=1. Values 0 <= gamma < 1 detect
        larger modules while gamma > 1 detects smaller modules.
    seed : hashable, optional
        If None (default), use the np.random's global random state to generate random numbers.
        Otherwise, use a new np.random.RandomState instance seeded with the given value.

    Returns
    -------
    ci : Nx1 np.ndarray
        refined community affiliation vector
    Q : float
        optimized modularity metric

    Notes
    -----
    Ci and Q may vary from run to run, due to heuristics in the
    algorithm. Consequently, it may be worth to compare multiple runs.
    """
    rng = get_rng(seed)
    n = len(W)
    if ci is None:
        ci = np.arange(n) + 1
    else:
        _, ci = np.unique(ci, return_inverse=True)
        ci += 1
    s = np.sum(W)
    knm_o = np.zeros((n, n))
    knm_i = np.zeros((n, n))
    for m in range(np.max(ci)):
        knm_o[:, m] = np.sum((W[:, ci == m + 1]), axis=1)
        knm_i[:, m] = np.sum((W[ci == m + 1, :]), axis=0)

    k_o = np.sum(knm_o, axis=1)
    k_i = np.sum(knm_i, axis=1)
    km_o = np.sum(knm_o, axis=0)
    km_i = np.sum(knm_i, axis=0)
    flag = True
    while flag:
        flag = False
        for u in rng.permutation(n):
            ma = ci[u] - 1
            dq_o = knm_o[u, :] - knm_o[(u, ma)] + W[(u, u)] - gamma * k_o[u] * (km_i - km_i[ma] + k_i[u]) / s
            dq_i = knm_i[u, :] - knm_i[(u, ma)] + W[(u, u)] - gamma * k_i[u] * (km_o - km_o[ma] + k_o[u]) / s
            dq = (dq_o + dq_i) / 2
            dq[ma] = 0
            max_dq = np.max(dq)
            if max_dq > 1e-10:
                mb = np.argmax(dq)
                knm_o[:, mb] += W[u, :].T
                knm_o[:, ma] -= W[u, :].T
                knm_i[:, mb] += W[:, u]
                knm_i[:, ma] -= W[:, u]
                km_o[mb] += k_o[u]
                km_o[ma] -= k_o[u]
                km_i[mb] += k_i[u]
                km_i[ma] -= k_i[u]
                ci[u] = mb + 1
                flag = True

    _, ci = np.unique(ci, return_inverse=True)
    ci += 1
    m = np.max(ci)
    w = np.zeros((m, m))
    for u in range(m):
        for v in range(m):
            w[(u, v)] = np.sum(W[np.ix_(ci == u + 1, ci == v + 1)])

    q = np.trace(w) / s - gamma * np.sum(np.dot(w / s, w / s))
    return (ci, q)


@due.dcite((BibTeX(SUN2008)), description='Finetuned undirected modularity')
@due.dcite((BibTeX(RUBINOV2011)), description='Finetuned undirected modularity')
def modularity_finetune_und(W, ci=None, gamma=1, seed=None):
    """
    The optimal community structure is a subdivision of the network into
    nonoverlapping groups of nodes in a way that maximizes the number of
    within-group edges, and minimizes the number of between-group edges.
    The modularity is a statistic that quantifies the degree to which the
    network may be subdivided into such clearly delineated groups.

    This algorithm is inspired by the Kernighan-Lin fine-tuning algorithm
    and is designed to refine a previously detected community structure.

    Parameters
    ----------
    W : NxN np.ndarray
        undirected weighted/binary connection matrix
    ci : Nx1 np.ndarray | None
        initial community affiliation vector
    gamma : float
        resolution parameter. default value=1. Values 0 <= gamma < 1 detect
        larger modules while gamma > 1 detects smaller modules.
    seed : hashable, optional
        If None (default), use the np.random's global random state to generate random numbers.
        Otherwise, use a new np.random.RandomState instance seeded with the given value.

    Returns
    -------
    ci : Nx1 np.ndarray
        refined community affiliation vector
    Q : float
        optimized modularity metric

    Notes
    -----
    Ci and Q may vary from run to run, due to heuristics in the
    algorithm. Consequently, it may be worth to compare multiple runs.
    """
    rng = get_rng(seed)
    n = len(W)
    if ci is None:
        ci = np.arange(n) + 1
    else:
        _, ci = np.unique(ci, return_inverse=True)
        ci += 1
    s = np.sum(W)
    knm = np.zeros((n, n))
    for m in range(np.max(ci)):
        knm[:, m] = np.sum((W[:, ci == m + 1]), axis=1)

    k = np.sum(knm, axis=1)
    km = np.sum(knm, axis=0)
    flag = True
    while flag:
        flag = False
        for u in rng.permutation(n):
            ma = ci[u] - 1
            dq = knm[u, :] - knm[(u, ma)] + W[(u, u)] - gamma * k[u] * (km - km[ma] + k[u]) / s
            dq[ma] = 0
            max_dq = np.max(dq)
            if max_dq > 1e-10:
                mb = np.argmax(dq)
                knm[:, mb] += W[:, u]
                knm[:, ma] -= W[:, u]
                km[mb] += k[u]
                km[ma] -= k[u]
                ci[u] = mb + 1
                flag = True

    _, ci = np.unique(ci, return_inverse=True)
    ci += 1
    m = np.max(ci)
    w = np.zeros((m, m))
    for u in range(m):
        for v in range(m):
            wm = np.sum(W[np.ix_(ci == u + 1, ci == v + 1)])
            w[(u, v)] = wm
            w[(v, u)] = wm

    q = np.trace(w) / s - gamma * np.sum(np.dot(w / s, w / s))
    return (ci, q)


@due.dcite((BibTeX(SUN2008)), description='Finetuned directed signed modularity')
@due.dcite((BibTeX(RUBINOV2011)), description='Finetuned directed signed modularity')
def modularity_finetune_und_sign(W, qtype='sta', gamma=1, ci=None, seed=None):
    """
    The optimal community structure is a subdivision of the network into
    nonoverlapping groups of nodes in a way that maximizes the number of
    within-group edges, and minimizes the number of between-group edges.
    The modularity is a statistic that quantifies the degree to which the
    network may be subdivided into such clearly delineated groups.

    This algorithm is inspired by the Kernighan-Lin fine-tuning algorithm
    and is designed to refine a previously detected community structure.

    Parameters
    ----------
    W : NxN np.ndarray
        undirected weighted/binary connection matrix with positive and
        negative weights.
    qtype : str
        modularity type. Can be 'sta' (default), 'pos', 'smp', 'gja', 'neg'.
        See Rubinov and Sporns (2011) for a description.
    gamma : float
        resolution parameter. default value=1. Values 0 <= gamma < 1 detect
        larger modules while gamma > 1 detects smaller modules.
    ci : Nx1 np.ndarray | None
        initial community affiliation vector
    seed : hashable, optional
        If None (default), use the np.random's global random state to generate random numbers.
        Otherwise, use a new np.random.RandomState instance seeded with the given value.

    Returns
    -------
    ci : Nx1 np.ndarray
        refined community affiliation vector
    Q : float
        optimized modularity metric

    Notes
    -----
    Ci and Q may vary from run to run, due to heuristics in the
    algorithm. Consequently, it may be worth to compare multiple runs.
    """
    rng = get_rng(seed)
    n = len(W)
    if ci is None:
        ci = np.arange(n) + 1
    else:
        _, ci = np.unique(ci, return_inverse=True)
        ci += 1
    W0 = W * (W > 0)
    W1 = -W * (W < 0)
    s0 = np.sum(W0)
    s1 = np.sum(W1)
    Knm0 = np.zeros((n, n))
    Knm1 = np.zeros((n, n))
    for m in range(int(np.max(ci))):
        Knm0[:, m] = np.sum((W0[:, ci == m + 1]), axis=1)
        Knm1[:, m] = np.sum((W1[:, ci == m + 1]), axis=1)

    Kn0 = np.sum(Knm0, axis=1)
    Kn1 = np.sum(Knm1, axis=1)
    Km0 = np.sum(Knm0, axis=0)
    Km1 = np.sum(Knm1, axis=0)
    if qtype == 'smp':
        d0 = 1 / s0
        d1 = 1 / s1
    else:
        if qtype == 'gja':
            d0 = 1 / (s0 + s1)
            d1 = 1 / (s0 + s1)
        else:
            if qtype == 'sta':
                d0 = 1 / s0
                d1 = 1 / (s0 + s1)
            else:
                if qtype == 'pos':
                    d0 = 1 / s0
                    d1 = 0
                else:
                    if qtype == 'neg':
                        d0 = 0
                        d1 = 1 / s1
                    else:
                        raise KeyError('modularity type unknown')
    if not s0:
        s0 = 1
        d0 = 0
    if not s1:
        s1 = 1
        d1 = 0
    flag = True
    h = 0
    while flag:
        h += 1
        if h > 1000:
            raise BCTParamError('Modularity infinite loop style D')
        flag = False
        for u in rng.permutation(n):
            ma = ci[u] - 1
            dq0 = Knm0[u, :] + W0[(u, u)] - Knm0[(u, ma)] - gamma * Kn0[u] * (Km0 + Kn0[u] - Km0[ma]) / s0
            dq1 = Knm1[u, :] + W1[(u, u)] - Knm1[(u, ma)] - gamma * Kn1[u] * (Km1 + Kn1[u] - Km1[ma]) / s1
            dq = d0 * dq0 - d1 * dq1
            dq[ma] = 0
            max_dq = np.max(dq)
            mb = np.argmax(dq)
            if max_dq > 1e-10:
                flag = True
                ci[u] = mb + 1
                Knm0[:, mb] += W0[:, u]
                Knm0[:, ma] -= W0[:, u]
                Knm1[:, mb] += W1[:, u]
                Knm1[:, ma] -= W1[:, u]
                Km0[mb] += Kn0[u]
                Km0[ma] -= Kn0[u]
                Km1[mb] += Kn1[u]
                Km1[ma] -= Kn1[u]

    _, ci = np.unique(ci, return_inverse=True)
    ci += 1
    m = np.tile(ci, (n, 1))
    q0 = (W0 - np.outer(Kn0, Kn0) / s0) * (m == m.T)
    q1 = (W1 - np.outer(Kn1, Kn1) / s1) * (m == m.T)
    q = d0 * np.sum(q0) - d1 * np.sum(q1)
    return (
     ci, q)


@due.dcite((BibTeX(BLONDEL2008)), description='Louvain directed modularity')
@due.dcite((BibTeX(REICHARDT2006)), description='Louvain directed modularity')
@due.dcite((BibTeX(RUBINOV2011)), description='Louvain directed modularity')
def modularity_louvain_dir(W, gamma=1, hierarchy=False, seed=None):
    """
    The optimal community structure is a subdivision of the network into
    nonoverlapping groups of nodes in a way that maximizes the number of
    within-group edges, and minimizes the number of between-group edges.
    The modularity is a statistic that quantifies the degree to which the
    network may be subdivided into such clearly delineated groups.

    The Louvain algorithm is a fast and accurate community detection
    algorithm (as of writing). The algorithm may also be used to detect
    hierarchical community structure.

    Parameters
    ----------
    W : NxN np.ndarray
        directed weighted/binary connection matrix
    gamma : float
        resolution parameter. default value=1. Values 0 <= gamma < 1 detect
        larger modules while gamma > 1 detects smaller modules.
    hierarchy : bool
        Enables hierarchical output. Defalut value=False
    seed : hashable, optional
        If None (default), use the np.random's global random state to generate random numbers.
        Otherwise, use a new np.random.RandomState instance seeded with the given value.

    Returns
    -------
    ci : Nx1 np.ndarray
        refined community affiliation vector. If hierarchical output enabled,
        it is an NxH np.ndarray instead with multiple iterations
    Q : float
        optimized modularity metric. If hierarchical output enabled, becomes
        an Hx1 array of floats instead.

    Notes
    -----
    Ci and Q may vary from run to run, due to heuristics in the
    algorithm. Consequently, it may be worth to compare multiple runs.
    """
    rng = get_rng(seed)
    n = len(W)
    s = np.sum(W)
    h = 0
    ci = []
    ci.append(np.arange(n) + 1)
    q = []
    q.append(-1)
    n0 = n
    while 1:
        if h > 300:
            raise BCTParamError('Modularity Infinite Loop Style E.  Please contact the developer with this error.')
        k_o = np.sum(W, axis=1)
        k_i = np.sum(W, axis=0)
        km_o = k_o.copy()
        km_i = k_i.copy()
        knm_o = W.copy()
        knm_i = W.copy()
        m = np.arange(n) + 1
        flag = True
        it = 0
        while flag:
            it += 1
            if it > 1000:
                raise BCTParamError('Modularity Infinite Loop Style F.  Please contact the developer with this error.')
            flag = False
            for u in rng.permutation(n):
                ma = m[u] - 1
                dq_o = knm_o[u, :] - knm_o[(u, ma)] + W[(u, u)] - gamma * k_o[u] * (km_i - km_i[ma] + k_i[u]) / s
                dq_i = knm_i[u, :] - knm_i[(u, ma)] + W[(u, u)] - gamma * k_i[u] * (km_o - km_o[ma] + k_o[u]) / s
                dq = (dq_o + dq_i) / 2
                dq[ma] = 0
                max_dq = np.max(dq)
                if max_dq > 1e-10:
                    mb = np.argmax(dq)
                    knm_o[:, mb] += W[u, :].T
                    knm_o[:, ma] -= W[u, :].T
                    knm_i[:, mb] += W[:, u]
                    knm_i[:, ma] -= W[:, u]
                    km_o[mb] += k_o[u]
                    km_o[ma] -= k_o[u]
                    km_i[mb] += k_i[u]
                    km_i[ma] -= k_i[u]
                    m[u] = mb + 1
                    flag = True

        _, m = np.unique(m, return_inverse=True)
        m += 1
        h += 1
        ci.append(np.zeros((n0,)))
        for i in range(n):
            ci[h][np.where(ci[(h - 1)] == i + 1)] = m[i]

        n = np.max(m)
        W1 = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                W1[(i, j)] = np.sum(W[np.ix_(m == i + 1, m == j + 1)])

        q.append(0)
        q[h] = np.trace(W1) / s - gamma * np.sum(np.dot(W1 / s, W1 / s))
        if q[h] - q[(h - 1)] < 1e-10:
            break

    ci = np.array(ci, dtype=int)
    if hierarchy:
        ci = ci[1:-1]
        q = q[1:-1]
        return (ci, q)
    return (ci[(h - 1)], q[(h - 1)])


@due.dcite((BibTeX(BLONDEL2008)), description='Louvain undirected modularity')
@due.dcite((BibTeX(REICHARDT2006)), description='Louvain undirected modularity')
@due.dcite((BibTeX(RUBINOV2011)), description='Louvain undirected modularity')
def modularity_louvain_und(W, gamma=1, hierarchy=False, seed=None):
    """
    The optimal community structure is a subdivision of the network into
    nonoverlapping groups of nodes in a way that maximizes the number of
    within-group edges, and minimizes the number of between-group edges.
    The modularity is a statistic that quantifies the degree to which the
    network may be subdivided into such clearly delineated groups.

    The Louvain algorithm is a fast and accurate community detection
    algorithm (as of writing). The algorithm may also be used to detect
    hierarchical community structure.

    Parameters
    ----------
    W : NxN np.ndarray
        undirected weighted/binary connection matrix
    gamma : float
        resolution parameter. default value=1. Values 0 <= gamma < 1 detect
        larger modules while gamma > 1 detects smaller modules.
    hierarchy : bool
        Enables hierarchical output. Defalut value=False
    seed : hashable, optional
        If None (default), use the np.random's global random state to generate random numbers.
        Otherwise, use a new np.random.RandomState instance seeded with the given value.

    Returns
    -------
    ci : Nx1 np.ndarray
        refined community affiliation vector. If hierarchical output enabled,
        it is an NxH np.ndarray instead with multiple iterations
    Q : float
        optimized modularity metric. If hierarchical output enabled, becomes
        an Hx1 array of floats instead.

    Notes
    -----
    Ci and Q may vary from run to run, due to heuristics in the
    algorithm. Consequently, it may be worth to compare multiple runs.
    """
    rng = get_rng(seed)
    n = len(W)
    s = np.sum(W)
    h = 0
    ci = []
    ci.append(np.arange(n) + 1)
    q = []
    q.append(-1)
    n0 = n
    while 1:
        if h > 300:
            raise BCTParamError('Modularity Infinite Loop Style B.  Please contact the developer with this error.')
        k = np.sum(W, axis=0)
        Km = k.copy()
        Knm = W.copy()
        m = np.arange(n) + 1
        flag = True
        it = 0
        while flag:
            it += 1
            if it > 1000:
                raise BCTParamError('Modularity Infinite Loop Style C.  Please contact the developer with this error.')
            flag = False
            for i in rng.permutation(n):
                ma = m[i] - 1
                dQ = Knm[i, :] - Knm[(i, ma)] + W[(i, i)] - gamma * k[i] * (Km - Km[ma] + k[i]) / s
                dQ[ma] = 0
                max_dq = np.max(dQ)
                if max_dq > 1e-10:
                    j = np.argmax(dQ)
                    Knm[:, j] += W[:, i]
                    Knm[:, ma] -= W[:, i]
                    Km[j] += k[i]
                    Km[ma] -= k[i]
                    m[i] = j + 1
                    flag = True

        _, m = np.unique(m, return_inverse=True)
        m += 1
        h += 1
        ci.append(np.zeros((n0,)))
        for i in range(n):
            ci[h][np.where(ci[(h - 1)] == i + 1)] = m[i]

        n = np.max(m)
        W1 = np.zeros((n, n))
        for i in range(n):
            for j in range(i, n):
                wp = np.sum(W[np.ix_(m == i + 1, m == j + 1)])
                W1[(i, j)] = wp
                W1[(j, i)] = wp

        W = W1
        q.append(0)
        q[h] = np.trace(W) / s - gamma * np.sum(np.dot(W / s, W / s))
        if q[h] - q[(h - 1)] < 1e-10:
            break

    ci = np.array(ci, dtype=int)
    if hierarchy:
        ci = ci[1:-1]
        q = q[1:-1]
        return (ci, q)
    return (ci[(h - 1)], q[(h - 1)])


@due.dcite((BibTeX(BLONDEL2008)), description='Louvain undirected signed modularity')
@due.dcite((BibTeX(REICHARDT2006)), description='Louvain undirected signed modularity')
@due.dcite((BibTeX(RUBINOV2011)), description='Louvain undirected signed modularity')
def modularity_louvain_und_sign(W, gamma=1, qtype='sta', seed=None):
    """
    The optimal community structure is a subdivision of the network into
    nonoverlapping groups of nodes in a way that maximizes the number of
    within-group edges, and minimizes the number of between-group edges.
    The modularity is a statistic that quantifies the degree to which the
    network may be subdivided into such clearly delineated groups.

    The Louvain algorithm is a fast and accurate community detection
    algorithm (at the time of writing).

    Use this function as opposed to modularity_louvain_und() only if the
    network contains a mix of positive and negative weights.  If the network
    contains all positive weights, the output will be equivalent to that of
    modularity_louvain_und().

    Parameters
    ----------
    W : NxN np.ndarray
        undirected weighted/binary connection matrix with positive and
        negative weights
    qtype : str
        modularity type. Can be 'sta' (default), 'pos', 'smp', 'gja', 'neg'.
        See Rubinov and Sporns (2011) for a description.
    gamma : float
        resolution parameter. default value=1. Values 0 <= gamma < 1 detect
        larger modules while gamma > 1 detects smaller modules.
    seed : hashable, optional
        If None (default), use the np.random's global random state to generate random numbers.
        Otherwise, use a new np.random.RandomState instance seeded with the given value.

    Returns
    -------
    ci : Nx1 np.ndarray
        refined community affiliation vector
    Q : float
        optimized modularity metric

    Notes
    -----
    Ci and Q may vary from run to run, due to heuristics in the
    algorithm. Consequently, it may be worth to compare multiple runs.
    """
    rng = get_rng(seed)
    n = len(W)
    W0 = W * (W > 0)
    W1 = -W * (W < 0)
    s0 = np.sum(W0)
    s1 = np.sum(W1)
    if qtype == 'smp':
        d0 = 1 / s0
        d1 = 1 / s1
    else:
        if qtype == 'gja':
            d0 = 1 / (s0 + s1)
            d1 = d0
        else:
            if qtype == 'sta':
                d0 = 1 / s0
                d1 = 1 / (s0 + s1)
            else:
                if qtype == 'pos':
                    d0 = 1 / s0
                    d1 = 0
                else:
                    if qtype == 'neg':
                        d0 = 0
                        d1 = 1 / s1
                    else:
                        raise KeyError('modularity type unknown')
    if not s0:
        s0 = 1
        d0 = 0
    if not s1:
        s1 = 1
        d1 = 0
    h = 1
    nh = n
    ci = [None, np.arange(n) + 1]
    q = [-1, 0]
    while q[h] - q[(h - 1)] > 1e-10:
        if h > 300:
            raise BCTParamError('Modularity Infinite Loop Style A.  Please contact the developer with this error.')
        kn0 = np.sum(W0, axis=0)
        kn1 = np.sum(W1, axis=0)
        km0 = kn0.copy()
        km1 = kn1.copy()
        knm0 = W0.copy()
        knm1 = W1.copy()
        m = np.arange(nh) + 1
        flag = True
        it = 0
        while flag:
            it += 1
            if it > 1000:
                raise BCTParamError('Infinite Loop was detected and stopped. This was probably caused by passing in a directed matrix.')
            flag = False
            for u in rng.permutation(nh):
                ma = m[u] - 1
                dQ0 = knm0[u, :] + W0[(u, u)] - knm0[(u, ma)] - gamma * kn0[u] * (km0 + kn0[u] - km0[ma]) / s0
                dQ1 = knm1[u, :] + W1[(u, u)] - knm1[(u, ma)] - gamma * kn1[u] * (km1 + kn1[u] - km1[ma]) / s1
                dQ = d0 * dQ0 - d1 * dQ1
                dQ[ma] = 0
                max_dQ = np.max(dQ)
                if max_dQ > 1e-10:
                    flag = True
                    mb = np.argmax(dQ)
                    knm0[:, mb] += W0[:, u]
                    knm0[:, ma] -= W0[:, u]
                    knm1[:, mb] += W1[:, u]
                    knm1[:, ma] -= W1[:, u]
                    km0[mb] += kn0[u]
                    km0[ma] -= kn0[u]
                    km1[mb] += kn1[u]
                    km1[ma] -= kn1[u]
                    m[u] = mb + 1

        h += 1
        ci.append(np.zeros((n,)))
        _, m = np.unique(m, return_inverse=True)
        m += 1
        for u in range(nh):
            ci[h][np.where(ci[(h - 1)] == u + 1)] = m[u]

        nh = np.max(m)
        wn0 = np.zeros((nh, nh))
        wn1 = np.zeros((nh, nh))
        for u in range(nh):
            for v in range(u, nh):
                wn0[(u, v)] = np.sum(W0[np.ix_(m == u + 1, m == v + 1)])
                wn1[(u, v)] = np.sum(W1[np.ix_(m == u + 1, m == v + 1)])
                wn0[(v, u)] = wn0[(u, v)]
                wn1[(v, u)] = wn1[(u, v)]

        W0 = wn0
        W1 = wn1
        q.append(0)
        q0 = np.trace(W0) - np.sum(np.dot(W0, W0)) / s0
        q1 = np.trace(W1) - np.sum(np.dot(W1, W1)) / s1
        q[h] = d0 * q0 - d1 * q1

    _, ci_ret = np.unique((ci[(-1)]), return_inverse=True)
    ci_ret += 1
    return (
     ci_ret, q[(-1)])


@due.dcite((BibTeX(SUN2008)), description='Probabilistic finetuned undirected modularity')
@due.dcite((BibTeX(RUBINOV2011)), description='Probabilistic finetuned undirected modularity')
def modularity_probtune_und_sign(W, qtype='sta', gamma=1, ci=None, p=0.45, seed=None):
    """
    The optimal community structure is a subdivision of the network into
    nonoverlapping groups of nodes in a way that maximizes the number of
    within-group edges, and minimizes the number of between-group edges.
    The modularity is a statistic that quantifies the degree to which the
    network may be subdivided into such clearly delineated groups.
    High-modularity degeneracy is the presence of many topologically
    distinct high-modularity partitions of the network.

    This algorithm is inspired by the Kernighan-Lin fine-tuning algorithm
    and is designed to probabilistically refine a previously detected
    community by incorporating random node moves into a finetuning
    algorithm.

    Parameters
    ----------
    W : NxN np.ndarray
        undirected weighted/binary connection matrix with positive and
        negative weights
    qtype : str
        modularity type. Can be 'sta' (default), 'pos', 'smp', 'gja', 'neg'.
        See Rubinov and Sporns (2011) for a description.
    gamma : float
        resolution parameter. default value=1. Values 0 <= gamma < 1 detect
        larger modules while gamma > 1 detects smaller modules.
    ci : Nx1 np.ndarray | None
        initial community affiliation vector
    p : float
        probability of random node moves. Default value = 0.45
    seed : hashable, optional
        If None (default), use the np.random's global random state to generate random numbers.
        Otherwise, use a new np.random.RandomState instance seeded with the given value.

    Returns
    -------
    ci : Nx1 np.ndarray
        refined community affiliation vector
    Q : float
        optimized modularity metric

    Notes
    -----
    Ci and Q may vary from run to run, due to heuristics in the
    algorithm. Consequently, it may be worth to compare multiple runs.
    """
    rng = get_rng(seed)
    n = len(W)
    if ci is None:
        ci = np.arange(n) + 1
    else:
        _, ci = np.unique(ci, return_inverse=True)
        ci += 1
    W0 = W * (W > 0)
    W1 = -W * (W < 0)
    s0 = np.sum(W0)
    s1 = np.sum(W1)
    Knm0 = np.zeros((n, n))
    Knm1 = np.zeros((n, n))
    for m in range(int(np.max(ci))):
        Knm0[:, m] = np.sum((W0[:, ci == m + 1]), axis=1)
        Knm1[:, m] = np.sum((W1[:, ci == m + 1]), axis=1)

    Kn0 = np.sum(Knm0, axis=1)
    Kn1 = np.sum(Knm1, axis=1)
    Km0 = np.sum(Knm0, axis=0)
    Km1 = np.sum(Knm1, axis=0)
    if qtype == 'smp':
        d0 = 1 / s0
        d1 = 1 / s1
    else:
        if qtype == 'gja':
            d0 = 1 / (s0 + s1)
            d1 = 1 / (s0 + s1)
        else:
            if qtype == 'sta':
                d0 = 1 / s0
                d1 = 1 / (s0 + s1)
            else:
                if qtype == 'pos':
                    d0 = 1 / s0
                    d1 = 0
                else:
                    if qtype == 'neg':
                        d0 = 0
                        d1 = 1 / s1
                    else:
                        raise KeyError('modularity type unknown')
    if not s0:
        s0 = 1
        d0 = 0
    if not s1:
        s1 = 1
        d1 = 0
    for u in rng.permutation(n):
        ma = ci[u] - 1
        r = rng.random_sample() < p
        if r:
            mb = rng.randint(n)
        else:
            dq0 = Knm0[u, :] + W0[(u, u)] - Knm0[(u, ma)] - gamma * Kn0[u] * (Km0 + Kn0[u] - Km0[ma]) / s0
            dq1 = Knm1[u, :] + W1[(u, u)] - Knm1[(u, ma)] - gamma * Kn1[u] * (Km1 + Kn1[u] - Km1[ma]) / s1
            dq = d0 * dq0 - d1 * dq1
            dq[ma] = 0
            max_dq = np.max(dq)
            mb = np.argmax(dq)
        if not r:
            if max_dq > 1e-10:
                pass
            ci[u] = mb + 1
            Knm0[:, mb] += W0[:, u]
            Knm0[:, ma] -= W0[:, u]
            Knm1[:, mb] += W1[:, u]
            Knm1[:, ma] -= W1[:, u]
            Km0[mb] += Kn0[u]
            Km0[ma] -= Kn0[u]
            Km1[mb] += Kn1[u]
            Km1[ma] -= Kn1[u]

    _, ci = np.unique(ci, return_inverse=True)
    ci += 1
    m = np.tile(ci, (n, 1))
    q0 = (W0 - np.outer(Kn0, Kn0) / s0) * (m == m.T)
    q1 = (W1 - np.outer(Kn1, Kn1) / s1) * (m == m.T)
    q = d0 * np.sum(q0) - d1 * np.sum(q1)
    return (
     ci, q)


@due.dcite((BibTeX(LEICHT2008)), description='Undirected modularity')
@due.dcite((BibTeX(REICHARDT2006)), description='Undirected modularity')
@due.dcite((BibTeX(GOOD2010)), description='Undirected modularity')
def modularity_und(A, gamma=1, kci=None):
    """
    The optimal community structure is a subdivision of the network into
    nonoverlapping groups of nodes in a way that maximizes the number of
    within-group edges, and minimizes the number of between-group edges.
    The modularity is a statistic that quantifies the degree to which the
    network may be subdivided into such clearly delineated groups.

    Parameters
    ----------
    W : NxN np.ndarray
        undirected weighted/binary connection matrix
    gamma : float
        resolution parameter. default value=1. Values 0 <= gamma < 1 detect
        larger modules while gamma > 1 detects smaller modules.
    kci : Nx1 np.ndarray | None
        starting community structure. If specified, calculates the Q-metric
        on the community structure giving, without doing any optimzation.
        Otherwise, if not specified, uses a spectral modularity maximization
        algorithm.

    Returns
    -------
    ci : Nx1 np.ndarray
        optimized community structure
    Q : float
        maximized modularity metric

    Notes
    -----
    This algorithm is deterministic. The matlab function bearing this
    name incorrectly disclaims that the outcome depends on heuristics
    involving a random seed. The louvain method does depend on a random seed,
    but this function uses a deterministic modularity maximization algorithm.
    """
    from scipy import linalg
    n = len(A)
    k = np.sum(A, axis=0)
    m = np.sum(k)
    B = A - gamma * np.outer(k, k) / m
    init_mod = np.arange(n)
    modules = []

    def recur(module):
        n = len(module)
        modmat = B[module][:, module]
        modmat -= np.diag(np.sum(modmat, axis=0))
        vals, vecs = linalg.eigh(modmat)
        rlvals = np.real(vals)
        max_eigvec = _safe_squeeze(vecs[:, np.where(rlvals == np.max(rlvals))])
        if max_eigvec.ndim > 1:
            max_eigvec = max_eigvec[:, 0]
        else:
            mod_asgn = _safe_squeeze((max_eigvec >= 0) * 2 - 1)
            q = np.dot(mod_asgn, np.dot(modmat, mod_asgn))
            if q > 0:
                qmax = q
                np.fill_diagonal(modmat, 0)
                it = np.ma.masked_array(np.ones((n,)), False)
                mod_asgn_iter = mod_asgn.copy()
                while np.any(it):
                    q_iter = qmax - 4 * mod_asgn_iter * np.dot(modmat, mod_asgn_iter)
                    qmax = np.max(q_iter * it)
                    imax = np.argmax(q_iter * it)
                    mod_asgn_iter[imax] *= -1
                    it[imax] = np.ma.masked
                    if qmax > q:
                        q = qmax
                        mod_asgn = mod_asgn_iter

                if np.abs(np.sum(mod_asgn)) == n:
                    modules.append(np.array(module).tolist())
                    return
                mod1 = module[np.where(mod_asgn == 1)]
                mod2 = module[np.where(mod_asgn == -1)]
                recur(mod1)
                recur(mod2)
            else:
                modules.append(np.array(module).tolist())

    if kci is None:
        recur(init_mod)
        ci = ls2ci(modules)
    else:
        ci = kci
    s = np.tile(ci, (n, 1))
    q = np.sum(np.logical_not(s - s.T) * B / m)
    return (ci, q)


def modularity_und_sign(W, ci, qtype='sta'):
    """
    This function simply calculates the signed modularity for a given
    partition. It does not do automatic partition generation right now.

    Parameters
    ----------
    W : NxN np.ndarray
        undirected weighted/binary connection matrix with positive and
        negative weights
    ci : Nx1 np.ndarray
        community partition
    qtype : str
        modularity type. Can be 'sta' (default), 'pos', 'smp', 'gja', 'neg'.
        See Rubinov and Sporns (2011) for a description.

    Returns
    -------
    ci : Nx1 np.ndarray
        the partition which was input (for consistency of the API)
    Q : float
        maximized modularity metric

    Notes
    -----
    uses a deterministic algorithm
    """
    n = len(W)
    _, ci = np.unique(ci, return_inverse=True)
    ci += 1
    W0 = W * (W > 0)
    W1 = -W * (W < 0)
    s0 = np.sum(W0)
    s1 = np.sum(W1)
    Knm0 = np.zeros((n, n))
    Knm1 = np.zeros((n, n))
    for m in range(int(np.max(ci))):
        Knm0[:, m] = np.sum((W0[:, ci == m + 1]), axis=1)
        Knm1[:, m] = np.sum((W1[:, ci == m + 1]), axis=1)

    Kn0 = np.sum(Knm0, axis=1)
    Kn1 = np.sum(Knm1, axis=1)
    Km0 = np.sum(Knm0, axis=0)
    Km1 = np.sum(Knm1, axis=0)
    if qtype == 'smp':
        d0 = 1 / s0
        d1 = 1 / s1
    else:
        if qtype == 'gja':
            d0 = 1 / (s0 + s1)
            d1 = 1 / (s0 + s1)
        else:
            if qtype == 'sta':
                d0 = 1 / s0
                d1 = 1 / (s0 + s1)
            else:
                if qtype == 'pos':
                    d0 = 1 / s0
                    d1 = 0
                else:
                    if qtype == 'neg':
                        d0 = 0
                        d1 = 1 / s1
                    else:
                        raise KeyError('modularity type unknown')
    if not s0:
        s0 = 1
        d0 = 0
    if not s1:
        s1 = 1
        d1 = 0
    m = np.tile(ci, (n, 1))
    q0 = (W0 - np.outer(Kn0, Kn0) / s0) * (m == m.T)
    q1 = (W1 - np.outer(Kn1, Kn1) / s1) * (m == m.T)
    q = d0 * np.sum(q0) - d1 * np.sum(q1)
    return (
     ci, q)


@due.dcite((BibTeX(MEILA2007)), description='Partition distance')
def partition_distance(cx, cy):
    """
    This function quantifies the distance between pairs of community
    partitions with information theoretic measures.

    Parameters
    ----------
    cx : Nx1 np.ndarray
        community affiliation vector X
    cy : Nx1 np.ndarray
        community affiliation vector Y

    Returns
    -------
    VIn : Nx1 np.ndarray
        normalized variation of information
    MIn : Nx1 np.ndarray
        normalized mutual information

    Notes
    -----
    (Definitions:
       VIn = [H(X) + H(Y) - 2MI(X,Y)]/log(n)
       MIn = 2MI(X,Y)/[H(X)+H(Y)]
    where H is entropy, MI is mutual information and n is number of nodes)
    """
    n = np.size(cx)
    _, cx = np.unique(cx, return_inverse=True)
    _, cy = np.unique(cy, return_inverse=True)
    _, cxy = np.unique((cx + cy * complex(0.0, 1.0)), return_inverse=True)
    cx += 1
    cy += 1
    cxy += 1
    Px = np.histogram(cx, bins=(np.max(cx)))[0] / n
    Py = np.histogram(cy, bins=(np.max(cy)))[0] / n
    Pxy = np.histogram(cxy, bins=(np.max(cxy)))[0] / n
    Hx = -np.sum(Px * np.log(Px))
    Hy = -np.sum(Py * np.log(Py))
    Hxy = -np.sum(Pxy * np.log(Pxy))
    Vin = (2 * Hxy - Hx - Hy) / np.log(n)
    Min = 2 * (Hx + Hy - Hxy) / (Hx + Hy)
    return (Vin, Min)