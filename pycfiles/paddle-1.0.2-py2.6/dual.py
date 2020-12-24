# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/paddle/dual.py
# Compiled at: 2011-02-18 07:33:24
"""
Implementation of PADDLE.

The two main functions are learn(), to actually run the algorithm, and init(),
to initialize the algorithm variables.

All other functions are internal, used in the implementation of the
above-mentioned two.
As such, their names begin with an underscore.
"""
import time
from scipy import linalg as la
from scipy import stats
import scipy as sp, pylab
from common import _cost_rec, _cost_cod, _replaceAtoms, _saveDict
from prox import _st
ra = sp.random

def _cost(X, U, D, C, pars):
    """
    Evaluation of the cost function.
    """
    full_out = {'rec_err': _cost_rec(D, X, U, pars), 
       'l1_pen': 2 * pars['tau'] * sp.absolute(U).mean(), 
       'l2_pen': pars['mu'] * (U ** 2).mean()}
    E = full_out['rec_err'] + full_out['l1_pen'] + full_out['l2_pen']
    if pars['eta'] > 0:
        full_out['cod_err'] = _cost_cod(C, X, U, pars)
        E += full_out['cod_err']
    return (
     E, full_out)


def _cost_fast(X, U, D, CX, pars):
    """
    Fast evaluation of the cost function.
    
    Computes the same cost function as in _cost, but exploits a precomputed
    CX and returns just the value of the whole cost function.
    """
    return ((X - sp.dot(D, U)) ** 2).mean() + pars['eta'] * ((U - CX) ** 2).mean() + 2 * pars['tau'] * sp.absolute(U).mean() + pars['mu'] * (U ** 2).mean()


def _ist_fixed(X, U0, D, C, pars, maxiter=1000):
    r"""
    Iterative soft-thresholding with fixed step-size.

    Minimization of :math:`\frac{1}{d}\|X-DU\|_F^2+\frac{\eta}{K}\|U-CX\|_F^2+\frac{2\tau}{K}\|U\|_1` wrt :math:`U`.
    When :math:`\eta=0` the functional reduces to the well-known LASSO.

    This function is curently noy used. The main function
    :func:`paddle.dual.learn` uses its FISTA-accelerated counterpart
    :func:`paddle.dual._pgd`.

    Parameters
    ----------
    X : (d, N) ndarray
        Data matrix
    U0 : (K, N) ndarray
        Initial value of the unknown 
    D : (d, K) ndarray
        Dictionary
    C : (K, d) ndarray
        Dual of the dictionary
    pars : dict
        Optional parameters
    maxiter : int
        Maximum number of iterations allowed (default 500)
        
    Returns
    -------
    U : (K, N) ndarray
        Optimal value of the unknown
    full_out : dict
        Full output
    """
    (d, N) = X.shape
    K = D.shape[1]
    U = U0.copy()
    DtD = sp.dot(D.T, D)
    ew = la.eigvalsh(DtD)
    sigma0 = (ew.min() + ew.max()) / (2 * N * d) + (pars['mu'] + pars['eta']) / (N * K)
    Y = U
    sigma = sigma0
    (E, full_out) = _cost(X, U, D, C, pars)
    print '   initial energy = %.5e' % E
    if pars['verbose']:
        print '   iter   energy   avg|upd|'
    DtD /= N * d * sigma
    DtX = sp.dot(D.T, X) / (N * d * sigma)
    CX = sp.dot(C, X)
    U0 = pars['eta'] * CX / (N * K * sigma) + DtX
    f = 1 - (pars['mu'] + pars['eta']) / (N * K * sigma)
    A = DtD - f * sp.identity(K)
    for i in xrange(maxiter):
        Unew = _st(U0 - sp.dot(A, Y), pars['tau'] / (N * K * sigma))
        E_new = _cost_fast(X, Unew, D, CX, pars)
        if i % 1 == 0 and pars['verbose']:
            upd = sp.sum((Unew - U) ** 2, 0) / sp.sum(U ** 2, 0)
            upd = upd[sp.isfinite(upd)]
            print '   %4d  %8.5e     %4.2f' % (i, E_new, upd.mean())
        Y = Unew
        U = Unew
        if sp.absolute(E - E_new) / E < pars['rtol']:
            break
        E = E_new

    print '   energy after %d iter. = %.5e' % (i + 1, E)
    (dummy, full_out) = _cost(X, Unew, D, C, pars)
    return (U, full_out)


def _ist(X, U0, D, C, pars, maxiter=1000):
    r"""
    Iterative soft-thresholding with FISTA acceleration.

    Minimization of :math:`\frac{1}{d}\|X-DU\|_F^2+\frac{\eta}{K}\|U-CX\|_F^2+\frac{2\tau}{K}\|U\|_1` wrt :math:`U`.
    When :math:`\eta=0` the functional reduces to the well-known LASSO.

    The function is used by :func:`paddle.dual.learn` for the optimization
    wrt ``U``.

    Parameters
    ----------
    X : (d, N) ndarray
        Data matrix
    U0 : (K, N) ndarray
        Initial value of the unknown 
    D : (d, K) ndarray
        Dictionary
    C : (K, d) ndarray
        Dual of the dictionary
    pars : dict
        Optional parameters
    maxiter : int
        Maximum number of iterations allowed (default 500)
        
    Returns
    -------
    U : (K, N) ndarray
        Optimal value of the unknown
    full_out : dict
        Full output
    """
    (d, N) = X.shape
    K = D.shape[1]
    (E, full_out) = _cost(X, U0, D, C, pars)
    print '   initial energy = %.5e' % E
    if pars['verbose']:
        print '   iter   energy   avg|upd|'
    DtD = sp.dot(D.T, D)
    ewmax = la.eigvalsh(DtD, eigvals=(K - 1, K - 1))
    sigma0 = ewmax / (N * d) + (pars['mu'] + pars['eta']) / (N * K)
    U = U0.copy()
    t = 1
    Y = U.copy()
    DtD /= N * d * sigma0
    DtX = sp.dot(D.T, X) / (N * d * sigma0)
    if C != None:
        CX = sp.dot(C, X)
    else:
        CX = sp.zeros(U.shape)
    U0 = pars['eta'] * CX / (N * K * sigma0) + DtX
    f = 1 - (pars['mu'] + pars['eta']) / (N * K * sigma0)
    A = DtD - f * sp.identity(K)
    for i in xrange(maxiter):
        Unew = _st(U0 - sp.dot(A, Y), pars['tau'] / (N * K * sigma0))
        if pars['nnU']:
            Unew = sp.clip(Unew, 0, sp.inf)
        E_new = _cost_fast(X, Unew, D, CX, pars)
        if i % 1 == 0 and pars['verbose']:
            upd = sp.sum((Unew - U) ** 2, 0) / sp.sum(U ** 2, 0)
            upd = upd[sp.isfinite(upd)]
            print '   %4d  %8.5e     %4.2f' % (i, E_new, upd.mean())
        tnew = (1 + sp.sqrt(1 + 4 * t ** 2)) / 2
        Y = Unew + (t - 1) / tnew * (Unew - U)
        t = tnew
        U = Unew
        if sp.absolute(E - E_new) / E < pars['rtol']:
            break
        E = E_new

    print '   energy after %d iter. = %.5e' % (i + 1, E)
    (dummy, full_out) = _cost(X, Unew, D, C, pars)
    return (U, full_out)


def _pgd_fixed(A0, X, U, B, G2, cost, maxiter=500, pars=None, sigma=None, axis=0, bound=1):
    """
    Projected gradient descent with fixed stepsize.
    """
    A = A0.copy()
    if sigma == None:
        ew = la.eigvalsh(G2)
        sigma = (ew.min() + ew.max()) / 2
    E = cost(A, X, U, pars)
    for j in xrange(maxiter):
        Anew = A + 1 / sigma * (B - sp.dot(A, G2))
        n = sp.sqrt(sp.sum(Anew ** 2, axis))
        newshape = [-1, -1]
        newshape[axis] = 1
        n.shape = newshape
        n = sp.where(n > bound, n, 1)
        Anew /= n
        Enew = cost(Anew, X, U, pars)
        if abs(Enew - E) / E < pars['rtol']:
            break
        A = Anew
        E = Enew

    return (
     A, j)


def _pgd(Y0, ABt, BBt, cost, maxiter=500, axis=0, bound=1, verbose=False, rtol=0.0001, nn=False):
    r"""
    Projected gradient descent with FISTA acceleration.

    Minimization of :math:`\|A-YB\|_F^2` wrt :math:`Y`, under additional
    constraints on the norms of the columns (or the rows) of :math:`Y`.
    The minimization is performed by alternatively descending along the
    gradient direction :math:`AB^T-YBB^T` and projecting the columns (rows)
    of :math:`Y` on the ball with given radius.

    The function is used by :func:`paddle.dual.learn` for the optimization
    wrt ``D`` and ``C``.
    In the former case, ``A`` and ``B`` are ``X`` and ``U``, respectively,
    while in the latter the roles are swapped.

    Parameters
    ----------
    Y0 : (a1, a2) ndarray
        Initial value of the unknown
    ABt : (a1, a2) ndarray
        Part of the gradient
    BBt : (a2, a2) ndarray
        Part of the gradient
    cost : function of type ``foo(Y)``
        Evaluates the cost function 
    maxiter : int
        Maximum number of iterations allowed (default 500)
    axis : int
        Dimension of ``Y`` along which the constraint is active (0 for cols, 1 for rows, default is 0)
    bound : float
        Value of the constraint on the norms of the columns/rows of ``Y`` (default is 1)
    verbose : bool
        If True displays the value of the cost function at each iteration (default is False)
    rtol : float
        Relative tolerance for convergence criterion
        
    Returns
    -------
    Y : () ndarray
        Optimal value of the unknown
    j : int
        Number of interations performed
    """
    E = cost(Y0)
    sigma = 2 * la.norm(BBt)
    Y = Y0.copy()
    t = 1
    Z = Y.copy()
    for j in xrange(maxiter):
        Ynew = Z + 1 / sigma * (ABt - sp.dot(Z, BBt))
        if nn:
            Ynew = sp.clip(Ynew, 0, sp.inf)
        if bound > 0:
            n = sp.sqrt(sp.sum(Ynew ** 2, axis))
            newshape = [
             -1, -1]
            newshape[axis] = 1
            n.shape = newshape
            n = sp.where(n > bound, n / bound, 1)
            Ynew /= n
        Enew = cost(Ynew)
        if verbose:
            print '   energy =', Enew
        if abs(Enew - E) / E < rtol:
            break
        tnew = (1 + sp.sqrt(1 + 4 * t ** 2)) / 2
        Z = Ynew + (t - 1) / tnew * (Ynew - Y)
        t = tnew
        Y = Ynew
        E = Enew

    return (
     Y, j)


def learn(X, D0, C0, U0, callable=None, **kwargs):
    """
    Runs the PADDLE algorithm.

    The function takes as input the data matrix ``X``, the initial
    values for the three unknowns, ``D0`` ``C0`` and ``U0``, and a dictionary
    of parameters.

    The optional parameters are passed as keyword arguments.

    Parameters
    ----------
    X : (d, N) ndarray
        Input data
    D0 : (d, K) ndarray
        The initial dictionary
    C0 : (K, d) ndarray
        The initial dual
    U0 : (K, N) ndarray
        The initial encodings
    callable : function of type foo(D, C, U, X)
        If not None, it gets called at each iteration and the result is
        appended in an item of full_output
    tau : float, optional
          Weight of the sparsity penalty (default 0.1)
    eta : float, optional
          Weight of the coding error (default 1.0)
    mu : float, optional
          Weight of the l2 penalty on the coefficients (default 0.0)
    nnU : bool, optional
          Adds a non-negativity constraint on U (default False)
    nnD : bool, optional
          Adds a non-negativity constraint on U (default False)
    maxiter : int, optional
          Maximum number of outer iterations (default 10)
    minused : integer, optional
          Minimum number of times an atom as to be used (default 1)
    verbose : bool, optional
          Enables verbose output (default False)
    rtol : float, optional
          Relative tolerance checking convergence (default 1.e-4)
    save_dict : bool, optional
          If true, the dictionary is saved after each outer iteration (default False)
    save_path : str, optional
          The path in which to save the dictionary (relevant only if save_dict is True, default "./")
    save_sorted : bool, optional
          If true and if save_dict is also True, the atoms of dictionary are sorted wrt the usage in the sparse coding before being displayed and saved (default False)
    save_shape: integer pair, optional
          Numbers of (rows,cols) used to display the atoms of the dictionary (default (10,10))

    Returns
    -------

    D : (d, K) ndarray
        The final dictionary
    C : (K, d) ndarray
        The final dual
    U : (K, N) ndarray
        The final encodings
    full_out : dict
        Full output
    """
    time0 = time.time()
    pars = {'maxiter': 10, 
       'minused': 1, 
       'tau': 0.1, 
       'eta': 1.0, 
       'mu': 0.0, 
       'nnU': False, 
       'nnD': False, 
       'Cbound': 1.0, 
       'verbose': False, 
       'rtol': 0.0001, 
       'save_dict': False, 
       'save_path': './', 
       'save_sorted': False, 
       'save_shape': (10, 10)}
    for key in kwargs:
        if key not in pars:
            raise ValueError, "User-defined parameter '%s' is not known" % key
        if key in pars:
            if isinstance(pars[key], float):
                kwargs[key] = float(kwargs[key])

    pars.update(kwargs)
    C, D, U = C0, D0, U0
    (d, N) = X.shape
    K = D.shape[1]
    XXt = sp.dot(X, X.T)
    (E, full_out0) = _cost(X, U, D, C, pars)
    print
    print ' Initial energy = %.5e' % E
    if callable != None:
        call_res = [
         callable(D, C, U, X)]
    Ehist = [E]
    timing = []
    for i in xrange(pars['maxiter']):
        print '  iter %d ------------' % i
        if pars['save_dict']:
            (rows, cols) = pars['save_shape']
            _saveDict(D, U, rows, cols, path=pars['save_path'] + 'dictD_' + str(i), sorted=pars['save_sorted'])
            _saveDict(C.T, U, rows, cols, path=pars['save_path'] + 'dictC_' + str(i), sorted=pars['save_sorted'])
        print '  optimizing U'
        start = time.time()
        (U, full_out) = _ist(X, U, D, C, pars, maxiter=1000)
        timeA = time.time() - start
        used = sp.where(sp.absolute(U) > 0, 1, 0)
        used_per_example = sp.sum(used, 0)
        print '  %.1f / %d non-zero coefficients per example (on avg)' % (
         used_per_example.mean(), U.shape[0])
        notused = sp.where(sp.sum(used, 1) < pars['minused'])[0]
        if len(notused) > 0:
            print '  %d atoms not used by at least %d examples' % (
             len(notused), pars['minused'])
            U = _replaceAtoms(X, U, D, notused)
        UUt = sp.dot(U, U.T)
        XUt = sp.dot(X, U.T)
        print '  Optimizing D'
        print '   reconstruction error = %.2e' % full_out['rec_err']
        start = time.time()

        def _costD(Y):
            return _cost_rec(Y, X, U)

        f = 1.0 / (N * d)
        (D, iters) = _pgd(D, f * XUt, f * UUt, _costD, verbose=pars['verbose'], rtol=pars['rtol'], nn=pars['nnD'])
        timeB = time.time() - start
        (E, full_out) = _cost(X, U, D, C, pars)
        print '   final reconstruction error = %.2e' % full_out['rec_err']
        print '   energy after %d iter. = %.5e' % (iters + 1, E)
        if pars['eta'] > 0:
            print '  Optimizing C'
            print '   coding error = %.2e' % full_out['cod_err']
            start = time.time()

            def _costC(Y):
                return _cost_cod(Y, X, U, pars)

            f = pars['eta'] / (N * K)
            (C, iters) = _pgd(C, f * XUt.T, f * XXt, _costC, axis=1, bound=pars['Cbound'], verbose=pars['verbose'], rtol=pars['rtol'])
            timeC = time.time() - start
            (E, full_out) = _cost(X, U, D, C, pars)
            print '   final coding error = %.2e' % full_out['cod_err']
            print '   energy after %d iter. = %.5e' % (iters + 1, E)
        else:
            timeC = 0
        if callable != None:
            call_res.append(callable(D, C, U, X))
        Em = sp.mean(Ehist[-min(len(Ehist), 3):])
        if abs(E - Em) / Em < 10.0 * pars['rtol']:
            break
        Ehist.append(E)
        full_out0 = full_out
        timing.append((timeA, timeB, timeC))

    print '  final --------------'
    used = sp.where(sp.absolute(U) > 0, 1, 0)
    l0 = used.flatten().sum()
    print '  %d / %d non-zero coefficients' % (l0, U.size)
    print '  average atom usage = %.1f' % sp.sum(used, 1).mean()
    timing.append(time.time() - time0)
    full_out['time'] = timing
    if callable != None:
        full_out['call_res'] = call_res
    full_out['iters'] = i
    return (
     D, C, U, full_out)


def init(X, K, det=False, rnd=False):
    """
    Initializes the variables.

    Initializes the matrices ``D``, ``C`` and ``U`` from the data matrix
    ``X``.
    The dimension of the dictionary is ``K``.
    If ``det`` is True the first ``K`` columns of ``X`` are chosen as
    atoms (deterministic initialization), otherwise they are picked 
    randomly.
    The atoms are normalized to one.
    The matrix ``U`` is chosen as to minimize the reconstruction error.
    The matrix ``C`` is chosen as the pseudo-inverse of ``D``, with
    rows normalized to one.

    Parameters
    ----------
    X : (d, N) ndarray
        Input data
    K : integer
        Size of the dictionary
    det : bool
        If True, the choice of atoms is deterministic
    rnd : bool
        If True, the atoms are not sampled from the examples, but have random values
    
    Returns
    -------
    D0 : (d, K) ndarray
        The initial dictionary
    C0 : (K, d) ndarray
        The initial dual
    U0 : (K, N) ndarray
        The initial encodings
    """
    (d, N) = X.shape
    if rnd:
        D0 = sp.random.rand(d, K)
    else:
        nonzero = sp.where(sp.sum(X ** 2, 0) > 0)[0]
        if det:
            sample = nonzero[:K]
        else:
            sample = sp.random.permutation(len(nonzero))[:K]
            sample = nonzero[sample]
        D0 = X[:, sample]
    D0 /= sp.sqrt(sp.sum(D0 ** 2, 0)).reshape((1, -1))
    pinv = la.pinv(D0)
    U0 = sp.dot(pinv, X)
    C0 = pinv / sp.sqrt(sp.sum(pinv ** 2, 1)).reshape((-1, 1))
    return (D0, C0, U0)


if __name__ == '__main__':
    N = 1500
    K = 50
    k = 3
    d = 20
    NMF = True
    if NMF:
        D_true = ra.uniform(0, 1, size=(d, K)).astype(sp.float32)
    else:
        D_true = ra.uniform(-1, 1, size=(d, K)).astype(sp.float32)
    D_true /= sp.sqrt(sp.sum(D_true ** 2, 0)).reshape((1, -1))
    U_true = sp.zeros((K, N), sp.float32)
    for i in xrange(N):
        if NMF:
            U_true[(ra.permutation(K)[:k], i)] = ra.uniform(0, 1, size=(k,))
        else:
            U_true[(ra.permutation(K)[:k], i)] = ra.uniform(-1, 1, size=(k,))

    assert sp.all(sp.sum(sp.where(sp.absolute(U_true) > 0, 1, 0), 0) == k)
    X = sp.dot(D_true, U_true)
    assert X.shape == (d, N)
    noise = ra.normal(0, 0.007, size=(d, N))
    SNR = la.norm(X) / la.norm(noise)
    print 'SNR (dB) = %d' % (20 * sp.log10(SNR),)
    X += noise
    (D0, C0, U0) = init(X, K)
    tau = 0.1
    mu = 1e-08
    eta = 0.0
    maxiter = 80
    (D, C, U, full_out) = learn(X, D0, C0, U0, tau=tau, mu=mu, eta=eta, maxiter=maxiter)
    print
    print sp.sum(D ** 2, 0).mean()
    D /= sp.sqrt(sp.sum(D ** 2, 0)).reshape((1, -1))
    print sp.sum(D ** 2, 0).mean()
    print sp.sum(D_true ** 2, 0).mean()
    d2 = sp.sum((D[:, :, sp.newaxis] - D_true[:, sp.newaxis, :]) ** 2, 0)
    closest = sp.argmin(d2, 0)
    dist = 1 - sp.absolute(sp.sum(D[:, closest] * D_true, 0))
    print dist
    print sp.where(dist < 0.01)
    print len(sp.where(dist < 0.01)[0])
    if NMF:
        print sp.where(U < 0), sp.where(D < 0)
        (D, C, U, full_out) = learn(X, D0, C0, U0, tau=tau, mu=mu, eta=eta, maxiter=maxiter, nnU=True, nnD=True, verbose=False)
        print sp.where(U < 0), sp.where(D < 0)
        d2 = sp.sum((D[:, :, sp.newaxis] - D_true[:, sp.newaxis, :]) ** 2, 0)
        closest = sp.argmin(d2, 0)
        dist = 1 - sp.absolute(sp.sum(D[:, closest] * D_true, 0))
        print dist
        print sp.where(dist < 0.01)
        print len(sp.where(dist < 0.01)[0])