# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pips.py
# Compiled at: 2010-12-26 13:36:33
"""Python Interior Point Solver (PIPS).

Ported by Richard Lincoln from the MATLAB Interior Point Solver (MIPS) (v1.9)
by Ray Zimmerman and released under the Apache License version 2.0 with his
written permission.  MIPS is distributed as part of the MATPOWER project,
developed at the Power System Engineering Research Center (PSERC), Cornell. See
U{http://www.pserc.cornell.edu/matpower/} for more info.
"""
from numpy import array, flatnonzero, Inf, any, isnan, ones, r_, finfo, zeros, dot, absolute
from numpy.linalg import norm
from scipy.sparse import csr_matrix, vstack, hstack, eye
from scipy.sparse.linalg import spsolve
EPS = finfo(float).eps

def pips(f_fcn, x0, A=None, l=None, u=None, xmin=None, xmax=None, gh_fcn=None, hess_fcn=None, opt=None):
    """Primal-dual interior point method for NLP (non-linear programming).
    Minimize a function F(X) beginning from a starting point M{x0}, subject to
    optional linear and non-linear constraints and variable bounds::

            min f(x)
             x

    subject to::

            g(x) = 0            (non-linear equalities)
            h(x) <= 0           (non-linear inequalities)
            l <= A*x <= u       (linear constraints)
            xmin <= x <= xmax   (variable bounds)

    Note: The calling syntax is almost identical to that of FMINCON from
    MathWorks' Optimization Toolbox. The main difference is that the linear
    constraints are specified with C{A}, C{L}, C{U} instead of C{A}, C{B},
    C{Aeq}, C{Beq}. The functions for evaluating the objective function,
    constraints and Hessian are identical.

    Example from U{http://en.wikipedia.org/wiki/Nonlinear_programming}:
        >>> from numpy import array, r_, float64, dot
        >>> from scipy.sparse import csr_matrix
        >>> def f2(x):
        ...     f = -x[0] * x[1] - x[1] * x[2]
        ...     df = -r_[x[1], x[0] + x[2], x[1]]
        ...     # actually not used since 'hess_fcn' is provided
        ...     d2f = -array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], float64)
        ...     return f, df, d2f
        >>> def gh2(x):
        ...     h = dot(array([[1, -1, 1],
        ...                    [1,  1, 1]]), x**2) + array([-2.0, -10.0])
        ...     dh = 2 * csr_matrix(array([[ x[0], x[0]],
        ...                                [-x[1], x[1]],
        ...                                [ x[2], x[2]]]))
        ...     g = array([])
        ...     dg = None
        ...     return h, g, dh, dg
        >>> def hess2(x, lam):
        ...     mu = lam["ineqnonlin"]
        ...     a = r_[dot(2 * array([1, 1]), mu), -1, 0]
        ...     b = r_[-1, dot(2 * array([-1, 1]),mu),-1]
        ...     c = r_[0, -1, dot(2 * array([1, 1]),mu)]
        ...     Lxx = csr_matrix(array([a, b, c]))
        ...     return Lxx
        >>> x0 = array([1, 1, 0], float64)
        >>> solution = pips(f2, x0, gh_fcn=gh2, hess_fcn=hess2)
        >>> round(solution["f"], 11) == -7.07106725919
        True
        >>> solution["output"]["iterations"]
        8

    Ported by Richard Lincoln from the MATLAB Interior Point Solver (MIPS)
    (v1.9) by Ray Zimmerman.  MIPS is distributed as part of the MATPOWER
    project, developed at the Power System Engineering Research Center (PSERC),
    Cornell. See U{http://www.pserc.cornell.edu/matpower/} for more info.
    MIPS was ported by Ray Zimmerman from C code written by H. Wang for his
    PhD dissertation:
      - "On the Computation and Application of Multi-period
        Security-Constrained Optimal Power Flow for Real-time
        Electricity Market Operations", Cornell University, May 2007.

    See also:
      - H. Wang, C. E. Murillo-Sanchez, R. D. Zimmerman, R. J. Thomas,
        "On Computational Issues of Market-Based Optimal Power Flow",
        IEEE Transactions on Power Systems, Vol. 22, No. 3, Aug. 2007,
        pp. 1185-1193.

    All parameters are optional except C{f_fcn} and C{x0}.
    @param f_fcn: Function that evaluates the objective function, its gradients
                  and Hessian for a given value of M{x}. If there are
                  non-linear constraints, the Hessian information is provided
                  by the 'hess_fcn' argument and is not required here.
    @type f_fcn: callable
    @param x0: Starting value of optimization vector M{x}.
    @type x0: array
    @param A: Optional linear constraints.
    @type A: csr_matrix
    @param l: Optional linear constraints. Default values are M{-Inf}.
    @type l: array
    @param u: Optional linear constraints. Default values are M{Inf}.
    @type u: array
    @param xmin: Optional lower bounds on the M{x} variables, defaults are
                 M{-Inf}.
    @type xmin: array
    @param xmax: Optional upper bounds on the M{x} variables, defaults are
                 M{Inf}.
    @type xmax: array
    @param gh_fcn: Function that evaluates the optional non-linear constraints
                   and their gradients for a given value of M{x}.
    @type gh_fcn: callable
    @param hess_fcn: Handle to function that computes the Hessian of the
                     Lagrangian for given values of M{x}, M{lambda} and M{mu},
                     where M{lambda} and M{mu} are the multipliers on the
                     equality and inequality constraints, M{g} and M{h},
                     respectively.
    @type hess_fcn: callable
    @param opt: optional options dictionary with the following keys, all of
                which are also optional (default values shown in parentheses)
                  - C{verbose} (False) - Controls level of progress output
                    displayed
                  - C{feastol} (1e-6) - termination tolerance for feasibility
                    condition
                  - C{gradtol} (1e-6) - termination tolerance for gradient
                    condition
                  - C{comptol} (1e-6) - termination tolerance for
                    complementarity condition
                  - C{costtol} (1e-6) - termination tolerance for cost
                    condition
                  - C{max_it} (150) - maximum number of iterations
                  - C{step_control} (False) - set to True to enable step-size
                    control
                  - C{max_red} (20) - maximum number of step-size reductions if
                    step-control is on
                  - C{cost_mult} (1.0) - cost multiplier used to scale the
                    objective function for improved conditioning. Note: The
                    same value must also be passed to the Hessian evaluation
                    function so that it can appropriately scale the objective
                    function term in the Hessian of the Lagrangian.
    @type opt: dict

    @rtype: dict
    @return: The solution dictionary has the following keys:
               - C{x} - solution vector
               - C{f} - final objective function value
               - C{converged} - exit status
                   - True = first order optimality conditions satisfied
                   - False = maximum number of iterations reached
                   - None = numerically failed
               - C{output} - output dictionary with keys:
                   - C{iterations} - number of iterations performed
                   - C{hist} - dictionary of arrays with trajectories of the
                     following: feascond, gradcond, compcond, costcond, gamma,
                     stepsize, obj, alphap, alphad
                   - C{message} - exit message
               - C{lmbda} - dictionary containing the Langrange and Kuhn-Tucker
                 multipliers on the constraints, with keys:
                   - C{eqnonlin} - non-linear equality constraints
                   - C{ineqnonlin} - non-linear inequality constraints
                   - C{mu_l} - lower (left-hand) limit on linear constraints
                   - C{mu_u} - upper (right-hand) limit on linear constraints
                   - C{lower} - lower bound on optimization variables
                   - C{upper} - upper bound on optimization variables

    @license: Apache License version 2.0
    """
    nx = x0.shape[0]
    nA = A.shape[0] if A is not None else 0
    l = -Inf * ones(nA) if l is None else l
    u = Inf * ones(nA) if u is None else u
    xmin = -Inf * ones(x0.shape[0]) if xmin is None else xmin
    xmax = Inf * ones(x0.shape[0]) if xmax is None else xmax
    if gh_fcn is None:
        nonlinear = False
        gn = array([])
        hn = array([])
    else:
        nonlinear = True
    opt = {} if opt is None else opt
    if not opt.has_key('feastol'):
        opt['feastol'] = 1e-06
    if not opt.has_key('gradtol'):
        opt['gradtol'] = 1e-06
    if not opt.has_key('comptol'):
        opt['comptol'] = 1e-06
    if not opt.has_key('costtol'):
        opt['costtol'] = 1e-06
    if not opt.has_key('max_it'):
        opt['max_it'] = 150
    if not opt.has_key('max_red'):
        opt['max_red'] = 20
    if not opt.has_key('step_control'):
        opt['step_control'] = False
    if not opt.has_key('cost_mult'):
        opt['cost_mult'] = 1
    if not opt.has_key('verbose'):
        opt['verbose'] = False
    hist = {}
    xi = 0.99995
    sigma = 0.1
    z0 = 1
    alpha_min = 1e-08
    mu_threshold = 1e-05
    i = 0
    converged = False
    eflag = False
    eyex = eye(nx, nx, format='csr')
    AA = eyex if A is None else vstack([eyex, A], 'csr')
    ll = r_[(xmin, l)]
    uu = r_[(xmax, u)]
    ieq = flatnonzero(absolute(uu - ll) <= EPS)
    igt = flatnonzero((uu >= 10000000000.0) & (ll > -10000000000.0))
    ilt = flatnonzero((ll <= -10000000000.0) & (uu < 10000000000.0))
    ibx = flatnonzero((absolute(uu - ll) > EPS) & (uu < 10000000000.0) & (ll > -10000000000.0))
    Ae = AA[ieq, :] if len(ieq) else None
    if len(ilt) or len(igt) or len(ibx):
        idxs = [
         (
          1, ilt), (-1, igt), (1, ibx), (-1, ibx)]
        Ai = vstack([ sig * AA[idx, :] for (sig, idx) in idxs if len(idx) ])
    else:
        Ai = None
    be = uu[ieq, :]
    bi = r_[(uu[ilt], -ll[igt], uu[ibx], -ll[ibx])]
    x = x0
    (f, df, _) = f_fcn(x)
    f = f * opt['cost_mult']
    df = df * opt['cost_mult']
    if nonlinear:
        (hn, gn, dhn, dgn) = gh_fcn(x)
        h = hn if Ai is None else r_[(hn, Ai * x - bi)]
        g = gn if Ae is None else r_[(gn, Ae * x - be)]
        if dhn is None and Ai is None:
            dh = None
        elif dhn is None:
            dh = Ai.T
        elif Ae is None:
            dh = dhn
        else:
            dh = hstack([dhn, Ai.T])
        if dgn is None and Ae is None:
            dg = None
        elif dgn is None:
            dg = Ae.T
        elif Ae is None:
            dg = dgn
        else:
            dg = hstack([dgn, Ae.T])
    else:
        h = -bi if Ai is None else Ai * x - bi
        g = -be if Ae is None else Ae * x - be
        dh = None if Ai is None else Ai.T
        dg = None if Ae is None else Ae.T
    neq = g.shape[0]
    niq = h.shape[0]
    neqnln = gn.shape[0]
    niqnln = hn.shape[0]
    nlt = len(ilt)
    ngt = len(igt)
    nbx = len(ibx)
    gamma = 1
    lam = zeros(neq)
    z = z0 * ones(niq)
    mu = z0 * ones(niq)
    k = flatnonzero(h < -z0)
    z[k] = -h[k]
    k = flatnonzero(gamma / z > z0)
    mu[k] = gamma / z[k]
    e = ones(niq)
    f0 = f
    Lx = df
    Lx = Lx + dg * lam if dg is not None else Lx
    Lx = Lx + dh * mu if dh is not None else Lx
    gnorm = norm(g, Inf) if len(g) else 0.0
    lam_norm = norm(lam, Inf) if len(lam) else 0.0
    mu_norm = norm(mu, Inf) if len(mu) else 0.0
    feascond = max([gnorm, max(h)]) / (1 + max([norm(x, Inf), norm(z, Inf)]))
    gradcond = norm(Lx, Inf) / (1 + max([lam_norm, mu_norm]))
    compcond = dot(z, mu) / (1 + norm(x, Inf))
    costcond = absolute(f - f0) / (1 + absolute(f0))
    hist[i] = {'feascond': feascond, 'gradcond': gradcond, 'compcond': compcond, 
       'costcond': costcond, 'gamma': gamma, 'stepsize': 0, 
       'obj': f / opt['cost_mult'], 'alphap': 0, 'alphad': 0}
    if opt['verbose']:
        print ' it    objective   step size   feascond     gradcond     compcond     costcond  '
        print '----  ------------ --------- ------------ ------------ ------------ ------------'
        print '%3d  %12.8g %10s %12g %12g %12g %12g' % (
         i, f / opt['cost_mult'], '',
         feascond, gradcond, compcond, costcond)
    if feascond < opt['feastol'] and gradcond < opt['gradtol'] and compcond < opt['comptol'] and costcond < opt['costtol']:
        converged = True
        if opt['verbose']:
            print 'Converged!'
    while not converged and i < opt['max_it']:
        i += 1
        lmbda = {'eqnonlin': lam[range(neqnln)], 'ineqnonlin': mu[range(niqnln)]}
        if nonlinear:
            if hess_fcn is None:
                print 'pips: Hessian evaluation via finite differences not yet implemented.\nPlease provide your own hessian evaluation function.'
            Lxx = hess_fcn(x, lmbda)
        else:
            (_, _, d2f) = f_fcn(x)
            Lxx = d2f * opt['cost_mult']
        rz = range(len(z))
        zinvdiag = csr_matrix((1.0 / z, (rz, rz))) if len(z) else None
        rmu = range(len(mu))
        mudiag = csr_matrix((mu, (rmu, rmu))) if len(mu) else None
        dh_zinv = None if dh is None else dh * zinvdiag
        M = Lxx if dh is None else Lxx + dh_zinv * mudiag * dh.T
        N = Lx if dh is None else Lx + dh_zinv * (mudiag * h + gamma * e)
        Ab = M if dg is None else vstack([
         hstack([M, dg]),
         hstack([dg.T, csr_matrix((neq, neq))])])
        bb = r_[(-N, -g)]
        dxdlam = spsolve(Ab.tocsr(), bb)
        dx = dxdlam[:nx]
        dlam = dxdlam[nx:nx + neq]
        dz = -h - z if dh is None else -h - z - dh.T * dx
        dmu = -mu if dh is None else -mu + zinvdiag * (gamma * e - mudiag * dz)
        if opt['step_control']:
            raise NotImplementedError
        k = flatnonzero(dz < 0.0)
        alphap = min([xi * min(z[k] / -dz[k]), 1]) if len(k) else 1.0
        k = flatnonzero(dmu < 0.0)
        alphad = min([xi * min(mu[k] / -dmu[k]), 1]) if len(k) else 1.0
        x = x + alphap * dx
        z = z + alphap * dz
        lam = lam + alphad * dlam
        mu = mu + alphad * dmu
        if niq > 0:
            gamma = sigma * dot(z, mu) / niq
        (f, df, _) = f_fcn(x)
        f = f * opt['cost_mult']
        df = df * opt['cost_mult']
        if nonlinear:
            (hn, gn, dhn, dgn) = gh_fcn(x)
            h = hn if Ai is None else r_[(hn, Ai * x - bi)]
            g = gn if Ae is None else r_[(gn, Ae * x - be)]
            if dhn is None and Ai is None:
                dh = None
            elif dhn is None:
                dh = Ai.T
            elif Ae is None:
                dh = dhn
            else:
                dh = hstack([dhn, Ai.T])
            if dgn is None and Ae is None:
                dg = None
            elif dgn is None:
                dg = Ae.T
            elif Ae is None:
                dg = dgn
            else:
                dg = hstack([dgn, Ae.T])
        else:
            h = -bi if Ai is None else Ai * x - bi
            g = -be if Ae is None else Ae * x - be
        Lx = df
        Lx = Lx + dg * lam if dg is not None else Lx
        Lx = Lx + dh * mu if dh is not None else Lx
        gnorm = norm(g, Inf) if len(g) else 0.0
        lam_norm = norm(lam, Inf) if len(lam) else 0.0
        mu_norm = norm(mu, Inf) if len(mu) else 0.0
        feascond = max([gnorm, max(h)]) / (1 + max([norm(x, Inf), norm(z, Inf)]))
        gradcond = norm(Lx, Inf) / (1 + max([lam_norm, mu_norm]))
        compcond = dot(z, mu) / (1 + norm(x, Inf))
        costcond = float(absolute(f - f0) / (1 + absolute(f0)))
        hist[i] = {'feascond': feascond, 'gradcond': gradcond, 'compcond': compcond, 
           'costcond': costcond, 'gamma': gamma, 'stepsize': norm(dx), 
           'obj': f / opt['cost_mult'], 'alphap': alphap, 
           'alphad': alphad}
        if opt['verbose']:
            print '%3d  %12.8g %10.5g %12g %12g %12g %12g' % (
             i, f / opt['cost_mult'], norm(dx), feascond, gradcond,
             compcond, costcond)
        if feascond < opt['feastol'] and gradcond < opt['gradtol'] and compcond < opt['comptol'] and costcond < opt['costtol']:
            converged = True
            if opt['verbose']:
                print 'Converged!'
        else:
            if any(isnan(x)) or alphap < alpha_min or alphad < alpha_min or gamma < EPS or gamma > 1.0 / EPS:
                if opt['verbose']:
                    print 'Numerically failed.'
                eflag = -1
                break
            f0 = f

    if opt['verbose']:
        if not converged:
            print 'Did not converge in %d iterations.' % i
    if eflag != -1:
        eflag = converged
    if eflag == 0:
        message = 'Did not converge'
    elif eflag == 1:
        message = 'Converged'
    elif eflag == -1:
        message = 'Numerically failed'
    else:
        raise
    output = {'iterations': i, 'history': hist, 'message': message}
    mu[flatnonzero((h < -opt['feastol']) & (mu < mu_threshold))] = 0.0
    f = f / opt['cost_mult']
    lam = lam / opt['cost_mult']
    mu = mu / opt['cost_mult']
    lam_lin = lam[neqnln:neq]
    mu_lin = mu[niqnln:niq]
    kl = flatnonzero(lam_lin < 0.0)
    ku = flatnonzero(lam_lin > 0.0)
    mu_l = zeros(nx + nA)
    mu_l[ieq[kl]] = -lam_lin[kl]
    mu_l[igt] = mu_lin[nlt:nlt + ngt]
    mu_l[ibx] = mu_lin[nlt + ngt + nbx:nlt + ngt + nbx + nbx]
    mu_u = zeros(nx + nA)
    mu_u[ieq[ku]] = lam_lin[ku]
    mu_u[ilt] = mu_lin[:nlt]
    mu_u[ibx] = mu_lin[nlt + ngt:nlt + ngt + nbx]
    lmbda = {'mu_l': mu_l[nx:], 'mu_u': mu_u[nx:], 'lower': mu_l[:nx], 
       'upper': mu_u[:nx]}
    if niqnln > 0:
        lmbda['ineqnonlin'] = mu[:niqnln]
    if neqnln > 0:
        lmbda['eqnonlin'] = lam[:neqnln]
    solution = {'x': x, 'f': f, 'converged': converged, 'lmbda': lmbda, 
       'output': output}
    return solution


def qps_pips(H, c, A, l, u, xmin=None, xmax=None, x0=None, opt=None):
    """Uses the Python Interior Point Solver (PIPS) to solve the following
    QP (quadratic programming) problem::

            min 1/2 x'*H*x + C'*x
             x

    subject to::

            l <= A*x <= u       (linear constraints)
            xmin <= x <= xmax   (variable bounds)

    Note the calling syntax is almost identical to that of QUADPROG from
    MathWorks' Optimization Toolbox. The main difference is that the linear
    constraints are specified with C{A}, C{L}, C{U} instead of C{A}, C{B},
    C{Aeq}, C{Beq}.

    See also L{pips}.

    Example from U{http://www.uc.edu/sashtml/iml/chap8/sect12.htm}:

        >>> from numpy import array, zeros, Inf
        >>> from scipy.sparse import csr_matrix
        >>> H = csr_matrix(array([[1003.1,  4.3,     6.3,     5.9],
        ...                       [4.3,     2.2,     2.1,     3.9],
        ...                       [6.3,     2.1,     3.5,     4.8],
        ...                       [5.9,     3.9,     4.8,     10 ]]))
        >>> c = zeros(4)
        >>> A = csr_matrix(array([[1,       1,       1,       1   ],
        ...                       [0.17,    0.11,    0.10,    0.18]]))
        >>> l = array([1, 0.10])
        >>> u = array([1, Inf])
        >>> xmin = zeros(4)
        >>> xmax = None
        >>> x0 = array([1, 0, 0, 1])
        >>> solution = qps_pips(H, c, A, l, u, xmin, xmax, x0)
        >>> round(solution["f"], 11) == 1.09666678128
        True
        >>> solution["converged"]
        True
        >>> solution["output"]["iterations"]
        10

    All parameters are optional except C{H}, C{C}, C{A} and C{L}.
    @param H: Quadratic cost coefficients.
    @type H: csr_matrix
    @param c: vector of linear cost coefficients
    @type c: array
    @param A: Optional linear constraints.
    @type A: csr_matrix
    @param l: Optional linear constraints. Default values are M{-Inf}.
    @type l: array
    @param u: Optional linear constraints. Default values are M{Inf}.
    @type u: array
    @param xmin: Optional lower bounds on the M{x} variables, defaults are
                 M{-Inf}.
    @type xmin: array
    @param xmax: Optional upper bounds on the M{x} variables, defaults are
                 M{Inf}.
    @type xmax: array
    @param x0: Starting value of optimization vector M{x}.
    @type x0: array
    @param opt: optional options dictionary with the following keys, all of
                which are also optional (default values shown in parentheses)
                  - C{verbose} (False) - Controls level of progress output
                    displayed
                  - C{feastol} (1e-6) - termination tolerance for feasibility
                    condition
                  - C{gradtol} (1e-6) - termination tolerance for gradient
                    condition
                  - C{comptol} (1e-6) - termination tolerance for
                    complementarity condition
                  - C{costtol} (1e-6) - termination tolerance for cost
                    condition
                  - C{max_it} (150) - maximum number of iterations
                  - C{step_control} (False) - set to True to enable step-size
                    control
                  - C{max_red} (20) - maximum number of step-size reductions if
                    step-control is on
                  - C{cost_mult} (1.0) - cost multiplier used to scale the
                    objective function for improved conditioning. Note: The
                    same value must also be passed to the Hessian evaluation
                    function so that it can appropriately scale the objective
                    function term in the Hessian of the Lagrangian.
    @type opt: dict

    @rtype: dict
    @return: The solution dictionary has the following keys:
               - C{x} - solution vector
               - C{f} - final objective function value
               - C{converged} - exit status
                   - True = first order optimality conditions satisfied
                   - False = maximum number of iterations reached
                   - None = numerically failed
               - C{output} - output dictionary with keys:
                   - C{iterations} - number of iterations performed
                   - C{hist} - dictionary of arrays with trajectories of the
                     following: feascond, gradcond, compcond, costcond, gamma,
                     stepsize, obj, alphap, alphad
                   - C{message} - exit message
               - C{lmbda} - dictionary containing the Langrange and Kuhn-Tucker
                 multipliers on the constraints, with keys:
                   - C{eqnonlin} - non-linear equality constraints
                   - C{ineqnonlin} - non-linear inequality constraints
                   - C{mu_l} - lower (left-hand) limit on linear constraints
                   - C{mu_u} - upper (right-hand) limit on linear constraints
                   - C{lower} - lower bound on optimization variables
                   - C{upper} - upper bound on optimization variables

    @license: Apache License version 2.0
    """
    if (H is None or H.nnz == 0) and (A is None or A.nnz == 0 and xmin is None or len(xmin) == 0 and xmax is None or len(xmax) == 0):
        print 'qps_pips: LP problem must include constraints or variable bounds'
        return
    else:
        if A is not None:
            if A.nnz >= 0:
                nx = A.shape[1]
            elif xmin is not None and len(xmin) > 0:
                nx = xmin.shape[0]
            elif xmax is not None and len(xmax) > 0:
                nx = xmax.shape[0]
            H = csr_matrix((nx, nx))
        else:
            nx = H.shape[0]
        xmin = -Inf * ones(nx) if xmin is None else xmin
        xmax = Inf * ones(nx) if xmax is None else xmax
        c = zeros(nx) if c is None else c
        x0 = zeros(nx) if x0 is None else x0
        opt = {} if opt is None else opt
        if not opt.has_key('cost_mult'):
            opt['cost_mult'] = 1

        def qp_f(x):
            f = 0.5 * dot(x.T * H, x) + dot(c.T, x)
            df = H * x + c
            d2f = H
            return (f, df, d2f)

        return pips(qp_f, x0, A, l, u, xmin, xmax, opt=opt)


if __name__ == '__main__':
    import doctest
    doctest.testmod()