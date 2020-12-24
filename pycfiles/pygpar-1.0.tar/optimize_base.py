# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pygp/optimize/optimize_base.py
# Compiled at: 2013-04-10 06:45:39
__doc__ = '\nPackage for Gaussian Process Optimization\n=========================================\n\nThis package provides optimization functionality\nfor hyperparameters of covariance functions\n:py:class:`pygp.covar` given. \n\n'
import scipy as SP, scipy.optimize as OPT, logging as LG, pdb, numpy, scipy.linalg
from scipy.linalg import LinAlgError
from scipy.optimize._minimize import minimize
import sys

def param_dict_to_list(di, skeys=None):
    """convert from param dictionary to list"""
    RV = numpy.concatenate([ di[key].ravel() for key in skeys ])
    return RV


def param_list_to_dict(li, param_struct, skeys):
    """convert from param dictionary to list
    param_struct: structure of parameter array
    """
    RV = []
    i0 = 0
    for key in skeys:
        val = param_struct[key]
        shape = SP.array(val)
        np = shape.prod()
        i1 = i0 + np
        params = li[i0:i1].reshape(shape)
        RV.append((key, params))
        i0 = i1

    return dict(RV)


def checkgrad(f, fprime, x, verbose=True, hyper_names=None, tolerance=0.1, *args, **kw_args):
    """
    Analytical gradient calculation using a 3-point method
    
    """
    import numpy as np
    eps = np.finfo(float).eps
    step = np.sqrt(eps)
    h = step * np.sign(np.random.uniform(-1, 1, x.shape))
    f_ph = f((x + h), *args, **kw_args)
    f_mh = f((x - h), *args, **kw_args)
    numerical_gradient = (f_ph - f_mh) / (2 * h)
    analytical_gradient_all = fprime(x, *args, **kw_args)
    h = np.zeros_like(x)
    dim = 1
    if f_ph.shape:
        dim = len(f_mh)
    res = np.zeros((len(x), 4, dim))
    if verbose:
        if hyper_names is None:
            hyper_names = map(str, range(len(x)))
        m = max_length(hyper_names)
        m = '{0!s:%is}' % m
        format_string = m + '  NUM:{1:13.5G}  ANA:{2:13.5G}  RAT:{3: 4.3F}  DIF:{4: 4.3F}'
    for i in range(len(x)):
        h[i] = step
        f_ph = f((x + h), *args, **kw_args)
        f_mh = f((x - h), *args, **kw_args)
        numerical_gradient = (f_ph - f_mh) / (2 * step)
        analytical_gradient = analytical_gradient_all[i]
        difference = numerical_gradient - analytical_gradient
        if np.abs(step * analytical_gradient) > 0:
            ratio = (f_ph - f_mh) / (2 * step * analytical_gradient)
        elif np.abs(difference) < tolerance:
            ratio = 1.0
        else:
            ratio = 0
        h[i] = 0
        if verbose:
            try:
                if np.abs(ratio - 1) < tolerance:
                    try:
                        mark = ' \x1b[92m✓\x1b[0m'
                    except:
                        mark = ':)'

                else:
                    try:
                        mark = ' \x1b[91m✗\x1b[0m'
                    except:
                        mark = 'X('

                print format_string.format(hyper_names[i], numerical_gradient, analytical_gradient, ratio, difference), mark
            except Exception:
                import ipdb
                ipdb.set_trace()

        res[i, 0, :] = numerical_gradient
        res[i, 1, :] = analytical_gradient
        res[i, 2, :] = ratio
        res[i, 3, :] = difference

    return res


def max_length(x_names):
    m = 0
    for name in x_names:
        m = max(m, len(str(name)))

    return m


def opt_hyper(gpr, hyperparams, Ifilter=None, maxiter=1000, gradcheck=False, bounds=None, callback=None, gradient_tolerance=1e-08, messages=True, *args, **kw_args):
    """
    Optimize hyperparemters of :py:class:`pygp.gp.basic_gp.GP` ``gpr`` starting from given hyperparameters ``hyperparams``.

    **Parameters:**

    gpr : :py:class:`pygp.gp.basic_gp`
        GP regression class
    hyperparams : {'covar':logtheta, ...}
        Dictionary filled with starting hyperparameters
        for optimization. logtheta are the CF hyperparameters.
    Ifilter : [boolean]
        Index vector, indicating which hyperparameters shall
        be optimized. For instance::

            logtheta = [1,2,3]
            Ifilter = [0,1,0]

        means that only the second entry (which equals 2 in
        this example) of logtheta will be optimized
        and the others remain untouched.

    bounds : [[min,max]]
        Array with min and max value that can be attained for any hyperparameter

    maxiter: int
        maximum number of function evaluations
    gradcheck: boolean 
        check gradients comparing the analytical gradients to their approximations
    
    ** argument passed onto LML**

    priors : [:py:class:`pygp.priors`]
        non-default prior, otherwise assume
        first index amplitude, last noise, rest:lengthscales
    """
    global __last_lml__
    __last_lml__ = 0

    def f(x):
        global __last_lml__
        x_ = X0
        x_[Ifilter_x] = x
        __last_lml__ = gpr.LML(param_list_to_dict(x_, param_struct, skeys), *args, **kw_args)
        if SP.isnan(__last_lml__):
            return 1000000.0
        return __last_lml__

    def df(x):
        x_ = X0
        x_[Ifilter_x] = x
        rv = gpr.LMLgrad(param_list_to_dict(x_, param_struct, skeys), *args, **kw_args)
        rv = param_dict_to_list(rv, skeys)
        if not SP.isfinite(rv).all():
            In = ~SP.isfinite(rv)
            rv[In] = 1000000.0
        return rv[Ifilter_x]

    skeys = SP.sort(hyperparams.keys())
    param_struct = dict([ (name, hyperparams[name].shape) for name in skeys ])
    X0 = param_dict_to_list(hyperparams, skeys)
    if Ifilter is not None:
        Ifilter_x = SP.array(param_dict_to_list(Ifilter, skeys), dtype='bool')
    else:
        Ifilter_x = slice(None)
    if bounds is not None:
        _b = []
        for key in skeys:
            if key in bounds.keys():
                _b.extend(bounds[key])
            else:
                _b.extend([(-SP.inf, +SP.inf)] * hyperparams[key].size)

        bounds = SP.array(_b)
        bounds = bounds[Ifilter_x]
    x = X0.copy()[Ifilter_x]
    LG.debug('startparameters for opt:' + str(x))
    if gradcheck:
        checkgrad(f, df, x, hyper_names=None)
        LG.info('check_grad (pre) (Enter to continue):' + str(OPT.check_grad(f, df, x)))
        raw_input()
    LG.debug('start optimization')
    try:
        iprint = -1
        if messages:
            iprint = 1
        res = minimize(f, x, method='L-BFGS-B', jac=df, bounds=bounds, callback=callback, tol=gradient_tolerance, options=dict(maxiter=maxiter, iprint=iprint))
        opt_RV, opt_lml = res.x, res.fun
        opt_x = opt_RV
    except LinAlgError as error:
        print error
        opt_x = X0
        opt_lml = __last_lml__

    Xopt = X0.copy()
    Xopt[Ifilter_x] = opt_x
    opt_hyperparams = param_list_to_dict(Xopt, param_struct, skeys)
    if gradcheck:
        checkgrad(f, df, Xopt, hyper_names=None)
        LG.info('check_grad (post) (Enter to continue):' + str(OPT.check_grad(f, df, opt_x)))
        pdb.set_trace()
    return [
     opt_hyperparams, opt_lml]