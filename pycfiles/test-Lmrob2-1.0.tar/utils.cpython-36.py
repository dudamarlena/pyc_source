# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nlrob/utils.py
# Compiled at: 2019-01-10 09:27:19
# Size of source mod 2**32: 26518 bytes
import types, numpy as np, re, patsy, ctypes, copy, os, sys, inspect, math, copy, scipy.integrate as integrate
from scipy.optimize import brentq, Bounds, minimize, curve_fit
from scipy.stats import norm
from numbers import Number
_Mpsi_R_names = [
 'bisquare', 'lqq', 'welsh', 'optimal', 'hampel', 'ggw']
_Mpsi_M_names = ['huber']
_Mpsi_names = _Mpsi_R_names + _Mpsi_M_names
_path_of_script = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))
_LMROBLIBPATH = os.path.join(_path_of_script, '../lmrob/liblmrob.so')
lmroblib = ctypes.cdll.LoadLibrary(_LMROBLIBPATH)

def _psi_conv_cc(psi, cc):
    if psi.lower() == 'ggw':
        if np.all(cc == np.array([-0.5, 1, 0.95, np.nan])):
            return 1
        else:
            if np.all(cc == np.array([-0.5, 1, 0.85, np.nan])):
                return 2
            else:
                if np.all(cc == np.array([-0.5, 1.0, np.nan, 0.5])):
                    return 3
                else:
                    if np.all(cc == np.array([-0.5, 1.5, 0.95, np.nan])):
                        return 4
                    if np.all(cc == np.array([-0.5, 1.5, 0.85, np.nan])):
                        return 5
                if np.all(cc == np.array([-0.5, 1.5, np.nan, 0.5])):
                    return 6
            return cc
    else:
        if psi.lower() == 'lqq':
            l = np.isnan(cc) == False
            if np.all(cc[l] == np.array([-0.5, 1.5, 0.95, np.nan])[l]):
                return np.array([1.4734061, 0.9822707, 1.5])
            else:
                if np.all(cc[l] == np.array([-0.5, 1.5, np.nan, 0.5])[l]):
                    return np.array([0.4015457, 0.2676971, 1.5])
                return cc
    return cc


def stopifnot(conditions):
    conditions = ''.join(conditions.split())
    split = conditions.split(',')
    for condition in conditions:
        assert eval(condition), '{:} is not True'.format(condition)


def sample(x, size=None):
    if not isinstance(x, (list, np.ndarray)):
        if size is None:
            xlen = x
        else:
            xlen = size
        np.random.permutation(x)[:xlen]
    else:
        if size is None:
            xlen = len(x)
        else:
            xlen = size
        indPerm = np.random.permutation(len(x))
        return x[indPerm]


def JDEoptim(lower, upper, fn, constr=None, meq=0, eps=1e-05, NP=None, Fl=0.1, Fu=1, tau_F=0.1, tau_CR=0.1, tau_pF=0.1, jitter_factor=0.001, tol=1e-15, maxiter=None, fnscale=1, compare_to=None, add_to_init_pop=None, trace=False, triter=1, details=False):
    r"""
    An implementation of a bespoke jDE variant of the Differential Evolution
    stochastic algorithm for global optimization of nonlinear programming
    problems

    Usage

    JDEoptim(lower, upper, fn,constr=None, meq=0, eps=1e-5,
             NP=None, Fl=0.1, Fu=1, tau_F=0.1, tau_CR=0.1,
             tau_pF=0.1, jitter_factor=0.001, tol=1e-15,
             maxiter=None, fnscale=1, compare_to=None,
             add_to_init_pop=None, trace=False, triter=1,
             details=False)
    
    Parameters
    ----------

    lower, upper: array_like
        numeric vectors of lower or upper bounds, respectively, for the
        parameters to be optimized over. Must be finite as they bound the hyper
        rectangle of the initial random population.
    fn: function
        (nonlinear) objective function to be minimized. It takes as first
        argument the vector of parameters over which minimization is to take
        place. It must return the value of the function at that point.
    constr: function
        an optional function for specifying the nonlinear constraints under
        which we want to minimize fn. They should be given in the form
        $h_i(x) = 0, g_i(x) \le 0$. This function takes the vector of parameters
        as its first argument and returns a real vector with the length of the
        total number of constraints. It defaults to None, meaning that
        bound-constrained minimization is used.
    meq: integer
        an optional positive integer specifying that the first meq constraints
        are treated as equality constraints, all the remaining as inequality
        constraints. Defaults to 0 (inequality constraints only).
    eps: float
        maximal admissible constraint violation for equality constraints. An
        optional real vector of small positive tolerance values with length meq
        used in the transformation of equalities into inequalities of the form
        $|h_i(x)| - \epsilon \le 0$. A scalar value is expanded to apply to all
        equality constraints. Default is 1e-5.
    NP: int
        an optional positive integer giving the number of candidate solutions in
        the randomly distributed initial population. Defaults to
        10*length(lower).
    FL: float
        an optional scalar which represents the minimum value that the scaling
        factor F could take. Default is 0.1, which is almost always satisfactory.
    Fu: float
        an optional scalar which represents the maximum value that the scaling
        factor F could take. Default is 1, which is almost always satisfactory.
    tau_F: float
        an optional scalar which represents the probability that the scaling
        factor F is updated. Defaults to 0.1, which is almost always
        satisfactory.
    tau_CR: float
        an optional scalar which represents the probability that the mutation
        probability $pF$ in the mutation strategy DE/rand/1/either-or is updated.
        Defaults to 0.1.
    jitter_factor: float    
        an optional tuning constant for jitter. If None L only dither is used.
        Defaults to 0.001.
    tol: float
        an optional positive scalar giving the tolerance for the stopping
        criterion. Default is 1e-15.
    maxiter: int
        an optional positive integer specifying the maximum number of iterations
        that may be performed before the algorithm is halted. Defaults to
        200*length(lower).
    fnscale: float
        an optional positive scalar specifying the typical magnitude of fn.
        It is used only in the stopping criterion. Defaults to 1. See ‘Details’.
    compare_to: str
        an optional character string controlling which function should be
        applied to the fn values of the candidate solutions in a generation to
        be compared with the so-far best one when evaluating the stopping
        criterion. If “median” the median function is used; else, if “max” the
        max function is used. It defaults to “median”.
    add_to_init_pop: array_like
        an optional real vector of length length(lower) or matrix with
        length(lower) rows specifying initial values of the parameters to be
        optimized which are appended to the randomly generated initial
        population. It defaults to None.
    trace: boolean
        an optional logical value indicating if a trace of the iteration
        progress should be printed. Default is False.
    triter: int
        an optional positive integer that controls the frequency of tracing when
        trace=True. Default is triter=1, which means that iteration: <value of
        stopping test> (value of best solution) best solution {index of
        violated constraints} is printed at every iteration.
    details: boolean        
        an optional logical value. If True the output will contain the
        parameters in the final population and their respective fn values.
        Defaults to False.

    Details
    -------
    The setting of the control parameters of standard Differential Evolution
    (DE) is crucial for the algorithm's performance. Unfortunately, when the
    generally recommended values for these parameters (see, e.g., Storn and
    Price, 1997) are unsuitable for use, their determination is often
    difficult and time consuming. The jDE algorithm proposed in Brest et al.
    (2006) employs a simple self-adaptive scheme to perform the automatic
    setting of control parameters scale factor F and crossover rate CR.

    This implementation differs from the original description, most notably
    in the use of the DE/rand/1/either-or mutation strategy (Price et al.,
    2005), combination of jitter with dither (Storn 2008), and its use of
    only a single population (Babu and Angira 2006) instead of separate
    current and child populations as in classical DE.

    Constraint handling is done using the approach described in Zhang and
    Rangaiah (2012), but with a different reduction updating scheme for the
    constraint relaxation value ($\mu$). Instead of doing it once for every
    generation or iteration, the reduction is triggered for two cases when
    the constraints only contain inequalities. Firstly, every time a
    feasible solution is selected for replacement in the next generation by
    a new feasible trial candidate solution with a better objective function
    value. Secondly, whenever a current infeasible solution gets replaced by
    a feasible one. If the constraints include equalities, then the
    reduction is not triggered in this last case. This constitutes an
    original feature of the implementation.

    Any DE variant is easily extended to deal with mixed integer nonlinear
    programming problems using a small variation of the technique presented by
    Lampinen and Zelinka (1999). Integer values are obtained by means of the
    floor() function only for the evaluation of the objective function. This is
    because DE itself works with continuous variables. Additionally, each upper
    bound of the integer variables should be added by 1.

    Notice that the final solution needs to be converted with floor() to obtain
    its integer elements.
    """
    np.random.seed(10000)

    def handle_bounds(x, u):
        bad = x > upper
        x[bad] = 0.5 * (upper[bad] + u[bad])
        bad = x < lower
        x[bad] = 0.5 * (lower[bad] + u[bad])
        return x

    def performReproduction():
        ignore = np.random.uniform(size=d) > CRtrial
        if np.all(ignore):
            ignore[sample(d)] = False
        else:
            if np.random.uniform(size=1)[0] <= pFtrial:
                trial = X_base + Ftrial * (X_r1 - X_r2)
            else:
                trial = X_base + 0.5 * (Ftrial + 1) * (X_r1 + X_r2 - 2 * X_base)
        trial[ignore] = X_i[ignore]
        return trial

    def which_best(x):
        if constr is not None:
            ind = TAVpop <= mu
            if np.all(ind):
                return np.argmin(x)
            else:
                if np.any(ind):
                    return np.where(ind)[np.argmin(x[ind])]
                return np.argmin(TAVpop)
        else:
            return np.argmin(x)

    compare_to_dict = {'median':np.median, 
     'max':np.max}
    compare_to = np.median if compare_to is None else compare_to_dict[compare_to]
    d = lower.size
    if len(upper) != d:
        raise Exception("'lower' must have same length as 'upper'")
    else:
        if NP is None:
            NP = 10 * d
        else:
            if maxiter is None:
                maxiter = 200 * d
            else:
                if constr is not None:
                    stopifnot('isinstance(constr, types.FunctionType)')
                    assert len(meq) == 1, 'len(meq) == 1 is not True'
                else:
                    if not meq == int(meq):
                        raise AssertionError('meq == int(meq) is not True')
                    else:
                        if not meq >= 0:
                            raise AssertionError('meq >= 0 is not True')
                        else:
                            if not np.isreal(eps):
                                raise AssertionError('np.isreal(eps) is not True')
                            else:
                                if not np.isfinite(eps):
                                    raise AssertionError('np.isfinite(eps) is not True')
                                else:
                                    if not eps > 0:
                                        raise AssertionError('eps > 0 is not True')
                                    else:
                                        if len(eps) == 1:
                                            eps = np.ones(meq) * eps
                                        else:
                                            if len(eps) != meq:
                                                raise Exception('eps must be either of length meq, or length 1')
                                            else:
                                                if not NP == int(NP):
                                                    raise AssertionError('NP == int(NP) is not True')
                                                elif not np.isreal(Fl):
                                                    raise AssertionError('np.isreal(Fl) is not True')
                                                assert np.isreal(Fu), 'np.isreal(Fu) is not True'
                                            assert Fl <= Fu, 'Fl <= Fu is not True'
                                        assert np.isreal(tau_F), 'np.isreal(tau_F) is not True'
                                    assert 0 <= tau_F, '0 <= tau_F is not True'
                                assert tau_F <= 1, 'tau_F <= 1 is not True'
                            assert np.isreal(tau_CR), 'np.isreal(tau_CR) is not True'
                        assert 0 <= tau_CR, '0 <= tau_CR is not True'
                    assert tau_CR <= 1, 'tau_CR <= 1 is not True'
                assert np.isreal(tau_pF), 'np.isreal(tau_pF) is not True'
            assert 0 <= tau_pF, '0 <= tau_pF is not True'
        assert tau_pF <= 1, 'tau_pF <= 1 is not True'
    if jitter_factor is not None:
        if not np.isreal(jitter_factor):
            raise AssertionError('np.isreal(jitter_factor) is not True')
    if add_to_init_pop is not None:
        if not add_to_init_pop.shape[0] == d:
            raise AssertionError('add_to_init_pop.shape[0] == d is not True')
        else:
            assert np.isreal(add_to_init_pop), 'np.isreal(add_to_init_pop) is not True'
            assert add_to_init_pop >= lower, 'add_to_init_pop >= lower is not True'
        if not add_to_init_pop <= upper:
            raise AssertionError('add_to_init_pop <= upper is not True')
    fn1 = lambda x: fn(x)
    if constr is not None:

        def constr1(x):
            if meq > 0:
                eqI = np.arange(meq)
                h = constr(x)
                h[eqI] = np.abs(h[eqI]) - eps
                return h
            else:
                return constr(x)

    else:
        use_jitter = jitter_factor is not None
        conv = lambda fpop, x_best_ind, fnscale: (compare_to(fpop) - fpop[x_best_ind]) / fnscale
        pop = np.random.uniform(np.min(lower), np.max(upper), (d, NP))
        if add_to_init_pop is not None:
            add_to_init_pop = add_to_init_pop.reshape(d, 1)
            pop = np.concatenate((pop, add_to_init_pop), axis=1)
            NP = pop.shape[1]
        if use_jitter:
            F = np.dot(1 + jitter_factor * np.random.uniform(-0.5, 0.5, (d, 1)), np.random.uniform(Fl, Fu, (1, NP)))
        else:
            F = np.random.uniform(Fl, Fu, (1, NP))
    CR = np.random.uniform(size=NP)
    pF = np.random.uniform(size=NP)
    fpop = np.apply_along_axis(fn1, 0, pop)
    if constr is not None:
        hpop = np.apply_along_axis(constr1, 0, pop)
        if np.any(np.isnan(hpop)):
            raise Exception('value of meq is invalid')
        TAVpop = np.apply_along_axis(lambda x: np.sum(np.maximum(x, 0)), 0, hpop)
        mu = np.median(TAVpop)
    popIndex = np.arange(NP)
    x_best_ind = which_best(fpop)
    converge = conv(fpop, x_best_ind, fnscale)

    def rule():
        if constr is not None:
            return converge >= tol or np.any(hpop[:, x_best_ind] > 0)
        else:
            return converge >= tol

    rule_condition = rule()
    converge = 0
    iteration = 0
    while rule_condition:
        if iteration >= maxiter:
            print('WARNING: maximum number of iterations reached without convergence')
            convergence = 1
            break
        iteration += 1
        for i in popIndex:
            ii = (iteration + i) % NP
            if np.random.uniform(size=1)[0] <= tau_F:
                if use_jitter:
                    Ftrial = np.random.uniform(Fl, Fu, 1)[0] * (1 + jitter_factor * np.random.uniform(-0.5, 0.5, d))
                else:
                    Ftrial = np.random.uniform(Fl, Fu, 1)
            else:
                Ftrial = F[:, ii]
            CRtrial = np.random.uniform(size=1)[0] if np.random.uniform(size=1)[0] <= tau_CR else CR[ii]
            pFtrial = np.random.uniform(size=1)[0] if np.random.uniform(size=1)[0] <= tau_pF else pF[ii]
            X_i = pop[:, ii]
            r = sample(np.array([j for j in popIndex if j != ii]), 3)
            X_base = pop[:, r[0]]
            X_r1 = pop[:, r[1]]
            X_r2 = pop[:, r[2]]
            trial = handle_bounds(performReproduction(), X_base)
            if constr is None:
                ftrial = fn1(trial)
                if ftrial <= fpop[ii]:
                    pop[:, ii] = trial
                    fpop[ii] = ftrial
                    F[:, ii] = Ftrial
                    CR[ii] = CRtrial
                    pF[ii] = pFtrial
            else:
                if meq > 0:
                    htrial = constr1(trial)
                    TAVtrial = np.sum(np.maximum(htrial, 0))
                    if TAVtrial > mu:
                        if TAVtrial <= TAVpop[ii]:
                            pop[:, ii] = trial
                            hpop[:, ii] = htrial
                            F[:, ii] = Ftrial
                            CR[ii] = CRtrial
                            pF[ii] = pFtrial
                            TAVpop[ii] = TAVtrial
                    else:
                        if TAVpop[ii] > mu:
                            pop[:, ii] = trial
                            fpop[ii] = fn1(trial)
                            hpop[:, ii] = htrial
                            F[:, ii] = Ftrial
                            CR[ii] = CRtrial
                            pF[ii] = pFtrial
                            TAVpop[ii] = TAVtrial
                        else:
                            ftrial = fn1(trial)
                    if ftrial <= fpop[ii]:
                        pop[:, ii] = trial
                        fpop[ii] = ftrial
                        hpop[:, ii] = htrial
                        F[:, ii] = Ftrial
                        CR[ii] = CRtrial
                        pF[ii] = pFtrial
                        TAVpop[ii] = TAVtrial
                        FF = np.sum(TAVpop <= mu) / NP
                        mu = mu * (1 - FF / NP)
                else:
                    htrial = constr1(trial)
                    TAVtrial = np.sum(np.maximum(htrial, 0))
                    if TAVtrial > mu:
                        if TAVtrial <= TAVpop[ii]:
                            pop[:, ii] = trial
                            hpop[:, ii] = htrial
                            F[:, ii] = Ftrial
                            CR[ii] = CRtrial
                            pF[ii] = pFtrial
                            TAVpop[ii] = TAVtrial
                    else:
                        if TAVpop[ii] > mu:
                            pop[:, ii] = trial
                            fpop[ii] = fn1(trial)
                            hpop[:, ii] = htrial
                            F[:, ii] = Ftrial
                            CR[ii] = CRtrial
                            pF[ii] = pFtrial
                            TAVpop[ii] = TAVtrial
                            FF = np.sum(TAVpop <= mu) / NP
                            mu = mu * (1 - FF / NP)
                        else:
                            ftrial = fn1(trial)
            if ftrial <= fpop[ii]:
                pop[:, ii] = trial
                fpop[ii] = ftrial
                hpop[:, ii] = htrial
                F[:, ii] = Ftrial
                CR[ii] = CRtrial
                pF[ii] = pFtrial
                TAVpop[ii] = TAVtrial
                FF = np.sum(TAVpop <= mu) / NP
                mu = mu * (1 - FF / NP)
            x_best_ind = which_best(fpop)

        converge = conv(fpop, x_best_ind, fnscale)
        rule_condition = rule()
        if trace and iteration % triter == 0:
            print(iteration, ':', '<', converge, '>', '(', fpop[x_best_ind], ')', pop[:, x_best_ind])

    dictReturn = {'par':pop[:, x_best_ind],  'value':fpop[x_best_ind], 
     'iter':iteration, 
     'convergence':converge}
    if details:
        dictReturn.update({'poppar':pop, 
         'popcost':fpop})
    return dictReturn


def Mchi(x, cc, psi, deriv=0):
    byref = ctypes.byref
    byref = ctypes.byref
    ipsi = ctypes.c_int(_psi2ipsi(psi))
    c_chi = ctypes.c_double(_psi_conv_cc(psi, cc))
    kernel_switch = {0:lmroblib.rho,  1:lmroblib.psi, 
     2:lmroblib.psip, 
     3:lmroblib.psi2}
    kernel = kernel_switch.get(deriv)
    kernel.argtypes = [ctypes.c_double,
     ctypes.POINTER(ctypes.c_double),
     ctypes.c_int]
    kernel.restype = ctypes.c_double
    values = np.array([kernel(res, byref(c_chi), ipsi) for res in x])
    if deriv > 0:
        rho_inf = lmroblib.rho_inf
        rho_inf.argtypes = [ctypes.POINTER(ctypes.c_double),
         ctypes.c_int]
        rho_inf.restype = ctypes.c_double
        return np.array([kernel(res, byref(c_chi), ipsi) / rho_inf(byref(c_chi), ipsi) for res in x])
    else:
        return np.array([kernel(res, byref(c_chi), ipsi) for res in x])


def lower_bound_from_vars(formula, variables):
    """
        Return the lower bound vector for the variables that don
    """
    formula_vars = get_vars_from_formula(formula)
    return np.array([0 for var in set(formula_vars) - set(variables) if var != ''])


def MrhoInf(cc, psi):
    rho_inf = lmroblib.rho_inf
    rho_inf.argtypes = [ctypes.POINTER(ctypes.c_double),
     ctypes.c_int]
    rho_inf.restype = ctypes.c_double
    cc_ = np.array([_psi_conv_cc(psi, cc)])
    cc_p = cc_.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    v = rho_inf(cc_p, _psi2ipsi(psi))
    return v


def get_vars_from_formula(formula, variables=[]):
    """
        Return the varnames of a given formula
    """
    math_operators = [
     '+', '-', '*', '**', '/', '(', ')', 'log', 'exp',
     'sin', 'cos', 'tan', 'np.']
    right_hand_term = formula.split('~')[1]
    for operator in math_operators:
        right_hand_term = right_hand_term.replace(operator, ' ')

    clean_variables = re.sub('(?<= )(\\d+)(?= )', '', right_hand_term)
    return np.array([var for var in set(clean_variables.split(' ')) - set(variables) if var != ''])


def _psi2ipsi(psi):
    psi = _regularize_Mpsi(psi, redescending=False)
    dictData = ['huber', 'bisquare', 'welsh', 'optimal', 'hampel', 'ggw', 'lqq']
    i = dictData.index(psi)
    if i is None:
        raise Exception('internal logic error in psi() function name: ', psi)
    return i


def _regularize_Mpsi(psi, redescending=True):
    psi = psi.lower()
    psi = {'tukey':'bisquare',  'biweight':'bisquare'}.get(psi, psi)
    nms = _Mpsi_R_names if redescending else _Mpsi_names
    if psi in nms:
        i = nms.index(psi)
    else:
        raise
    return nms[i]


def _convSS(ss):
    if ss == 'single':
        return 0
    if ss == 'nonsingular':
        return 1
    raise Exception("unknown setting for 'subsampling': %s" % ss)


def _Mpsi(x, c_chi_, ipsi_, deriv=0):
    if not isinstance(x, np.ndarray):
        x = np.array([x])
    byref = ctypes.byref
    ipsi = ctypes.c_int(ipsi_)
    c_chi_p = c_chi_.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    kernel_switch = {-1: lmroblib.rho, 
     0: lmroblib.psi, 
     1: lmroblib.psip, 
     2: lmroblib.psi2}
    kernel = kernel_switch.get(deriv)
    kernel.argtypes = [ctypes.c_double,
     ctypes.POINTER(ctypes.c_double),
     ctypes.c_int]
    kernel.restype = ctypes.c_double
    values = np.array([kernel(res, c_chi_p, ipsi) for res in x])
    if ipsi.value != 0 and deriv == -1:
        rho_inf = lmroblib.rho_inf
        rho_inf.argtypes = [ctypes.POINTER(ctypes.c_double),
         ctypes.c_int]
        rho_inf.restype = ctypes.c_double
        return np.array([kernel(res, c_chi_p, ipsi) * rho_inf(c_chi_p, ipsi) for res in x])
    else:
        return np.array([kernel(res, c_chi_p, ipsi) for res in x])


def _Mwgt(x, cc, psi):
    byref = ctypes.byref
    ipsi = ctypes.c_int(psi)
    c_chi = np.array([cc]).ravel()
    c_chi_p = c_chi.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    wgt = lmroblib.wgt
    wgt.argtypes = [ctypes.c_double,
     ctypes.POINTER(ctypes.c_double),
     ctypes.c_int]
    wgt.restype = ctypes.c_double
    rweights = np.array([wgt(res, c_chi_p, ipsi) for res in x])
    return rweights