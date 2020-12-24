# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/tom/.local/miniconda/lib/python3.6/site-packages/alphacsc/update_z.py
# Compiled at: 2019-06-04 04:10:26
# Size of source mod 2**32: 11390 bytes
import time, numpy as np
from scipy import linalg
from scipy import optimize, signal
from joblib import Parallel, delayed
from .utils.convolution import _choose_convolve
from .utils.optim import power_iteration
from .utils import check_consistent_shape

def update_z(X, ds, reg, z0=None, debug=False, parallel=None, solver='l-bfgs', b_hat_0=None, solver_kwargs=dict(), sample_weights=None):
    """Update Z using L-BFGS with positivity constraints

    Parameters
    ----------
    X : array, shape (n_trials, n_times)
        The data array
    ds : array, shape (n_atoms, n_times_atom)
        The atoms.
    reg : float
        The regularization constant
    z0 : None | array, shape (n_atoms, n_trials, n_times_valid)
        Init for z (can be used for warm restart).
    debug : bool
        If True, check the grad.
    parallel : instance of Parallel
        Context manager for running joblibs in a loop.
    solver : 'l-bfgs' | 'ista' | 'fista'
        The solver to use.
    b_hat_0 : array, shape ((n_times - n_times_atom + 1) * n_atoms)
        init vector for power_iteration with 'ista' solver
    solver_kwargs : dict
        Parameters for the solver
    sample_weights: array, shape (n_trials, n_times)
        Weights applied on the cost function.

    Returns
    -------
    z : array, shape (n_trials, n_times - n_times_atom + 1)
        The true codes.
    """
    n_trials, n_times = X.shape
    check_consistent_shape(X, sample_weights)
    n_atoms, n_times_atom = ds.shape
    n_times_valid = n_times - n_times_atom + 1
    my_update_z = delayed(_update_z_idx)
    if parallel is None:
        parallel = Parallel(n_jobs=1)
    else:
        assert parallel.n_jobs >= 1
    zhats = parallel(my_update_z(X, ds, reg, z0, i, debug, solver, b_hat_0, solver_kwargs, sample_weights) for i in np.array_split(np.arange(n_trials), parallel.n_jobs))
    z_hat = np.vstack(zhats)
    z_hat2 = z_hat.reshape((n_trials, n_atoms, n_times_valid))
    z_hat2 = np.swapaxes(z_hat2, 0, 1)
    return z_hat2


def _fprime(ds, zi, Xi=None, sample_weights=None, reg=None, return_func=False):
    """np.dot(D.T, X[i] - np.dot(D, zi)) + reg

    Parameters
    ----------
    ds : array, shape (n_atoms, n_times_atom)
        The atoms
    zi : array, shape (n_atoms * n_times_valid)
        The activations
    Xi : array, shape (n_times, ) or None
        The data array for one trial
    sample_weights : array, shape (n_times, ) or None
        The sample weights for one trial
    reg : float or None
        The regularization constant
    return_func : boolean
        Returns also the objective function, used to speed up LBFGS solver

    Returns
    -------
    (func) : float
        The objective function
    grad : array, shape (n_atoms * n_times_valid)
        The gradient
    """
    n_atoms, n_times_atom = ds.shape
    zi_reshaped = zi.reshape((n_atoms, -1))
    Dzi = _choose_convolve(zi_reshaped, ds)
    if Xi is not None:
        Dzi -= Xi
    else:
        if sample_weights is not None:
            if return_func:
                wDzi = sample_weights * Dzi
            else:
                Dzi *= sample_weights
                wDzi = Dzi
        else:
            wDzi = Dzi
    if return_func:
        func = 0.5 * np.dot(wDzi, Dzi.T)
        if reg is not None:
            func += reg * zi.sum()
    grad = np.concatenate([signal.convolve(wDzi, d[::-1], 'valid') for d in ds])
    if reg is not None:
        grad += reg
    if return_func:
        return (func, grad)
    else:
        return grad


def _update_z_idx(X, ds, reg, z0, idxs, debug, solver='l-bfgs', b_hat_0=None, solver_kwargs=dict(), sample_weights=None, timing=False):
    n_trials, n_times = X.shape
    n_atoms, n_times_atom = ds.shape
    n_times_valid = n_times - n_times_atom + 1
    bounds = [(0, None) for idx in range(n_atoms * n_times_valid)]
    zhats = []
    for i in idxs:
        if sample_weights is None:
            sample_weights_i = None
        else:
            sample_weights_i = sample_weights[i]

        def func_and_grad(zi):
            return _fprime(ds, zi, Xi=(X[i]), reg=reg, return_func=True, sample_weights=sample_weights_i)

        def grad_noreg(zi):
            return _fprime(ds, zi, Xi=(X[i]), reg=None, return_func=False, sample_weights=sample_weights_i)

        if z0 is None:
            f0 = np.zeros(n_atoms * n_times_valid)
        else:
            f0 = z0[:, i, :].reshape(n_atoms * n_times_valid)
        if timing:
            times = [
             0]
            pobj = [func_and_grad(f0)[0]]
            start = [time.time()]
        if debug:

            def pobj(zi):
                return func_and_grad(zi)[0]

            def fprime(zi):
                return func_and_grad(zi)[1]

            if not optimize.check_grad(pobj, fprime, f0) < 1e-05:
                raise AssertionError
        if solver == 'l-bfgs':
            if timing:

                def callback(xk):
                    times.append(time.time() - start[0])
                    pobj.append(func_and_grad(xk)[0])
                    start[0] = time.time()

            else:
                callback = None
            factr = solver_kwargs.get('factr', 1000000000000000.0)
            maxiter = solver_kwargs.get('maxiter', 15000)
            zhat, f, d = optimize.fmin_l_bfgs_b(func_and_grad, f0, fprime=None, args=(), approx_grad=False, bounds=bounds,
              factr=factr,
              maxiter=maxiter,
              callback=callback)
        else:
            if solver == 'ista':
                zhat = f0.copy()
                DTD = gram_block_circulant(ds, n_times_valid, 'custom', sample_weights=sample_weights_i)
                tol = solver_kwargs.get('power_iteration_tol', 0.0001)
                L = power_iteration(DTD, b_hat_0=b_hat_0, tol=tol)
                step_size = 0.99 / L
                max_iter = solver_kwargs.get('max_iter', 20)
                for k in range(max_iter):
                    zhat -= step_size * grad_noreg(zhat)
                    zhat = np.maximum(zhat - reg * step_size, 0.0)
                    if timing:
                        times.append(time.time() - start[0])
                        pobj.append(func_and_grad(zhat)[0])
                        start[0] = time.time()

            else:
                if solver == 'fista':
                    x_new = f0.copy()
                    y = x_new.copy()
                    t_new = 1.0
                    DTD = gram_block_circulant(ds, n_times_valid, 'custom', sample_weights=sample_weights_i)
                    tol = solver_kwargs.get('power_iteration_tol', 0.0001)
                    L = power_iteration(DTD, b_hat_0=b_hat_0, tol=tol)
                    step_size = 0.99 / L
                    max_iter = solver_kwargs.get('max_iter', 20)
                    restart = solver_kwargs.get('restart', None)
                    for k in range(max_iter):
                        if k > 0:
                            if restart is not None:
                                if k % restart == 0:
                                    y = x_new.copy()
                                    t_new = 1.0
                            t_old = t_new
                            x_old = x_new
                            y -= step_size * grad_noreg(y)
                            x_new = np.maximum(y - reg * step_size, 0.0)
                            t_new = 0.5 * (1.0 + np.sqrt(1.0 + 4.0 * t_old ** 2))
                            y = x_new + (t_old - 1.0) / t_new * (x_new - x_old)
                            if timing:
                                times.append(time.time() - start[0])
                                pobj.append(func_and_grad(x_new)[0])
                                start[0] = time.time()

                    zhat = x_new
                else:
                    raise ValueError("Unrecognized solver %s. Must be 'ista', 'fista', or 'l-bfgs'." % solver)
        zhats.append(zhat)

    if timing:
        return (np.vstack(zhats), pobj, times)
    else:
        return np.vstack(zhats)


def gram_block_circulant(ds, n_times_valid, method='full', sample_weights=None):
    """Returns ...

    Parameters
    ----------
    ds : array, shape (n_atoms, n_times_atom)
        The atoms
    n_times_valid : int
        n_times - n_times_atom + 1
    method : string
        If 'full', returns full circulant matrix.
        If 'scipy', returns scipy linear operator.
        If 'custom', returns custom linear operator.
    sample_weights : array, shape (n_times, )
        The sample weights for one trial
    """
    from scipy.sparse.linalg import LinearOperator
    from functools import partial
    n_atoms, n_times_atom = ds.shape
    n_times = n_times_valid + n_times_atom - 1
    if method == 'full':
        D = np.zeros((n_times, n_atoms * n_times_valid))
        for k_idx in range(n_atoms):
            d_padded = np.zeros((n_times,))
            d_padded[:n_times_atom] = ds[k_idx]
            start = k_idx * n_times_valid
            stop = start + n_times_valid
            D[:, start:stop] = linalg.circulant(d_padded)[:, :n_times_valid]

        if sample_weights is not None:
            wD = sample_weights[:, None] * D
            return np.dot(D.T, wD)
        else:
            return np.dot(D.T, D)
    else:
        if method == 'scipy':

            def matvec(v, ds):
                assert v.shape[0] % ds.shape[0] == 0
                return _fprime(ds, v, Xi=None, reg=None, sample_weights=sample_weights)

            D = LinearOperator((n_atoms * n_times_valid, n_atoms * n_times_valid), matvec=partial(matvec, ds=ds))
        else:
            if method == 'custom':
                return CustomLinearOperator(ds, n_times_valid, sample_weights)
            raise ValueError('Unkown method %s.' % method)
    return D


class CustomLinearOperator:
    """CustomLinearOperator"""

    def __init__(self, ds, n_times_valid, sample_weights):
        self.ds = ds
        product = ds.shape[0] * n_times_valid
        self.shape = (product, product)
        self.sample_weights = sample_weights

    def dot(self, v):
        ds = self.ds
        assert v.shape[0] % ds.shape[0] == 0
        return _fprime(ds, v, Xi=None, reg=None, sample_weights=(self.sample_weights))