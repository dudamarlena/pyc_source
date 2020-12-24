# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/sella/optimize.py
# Compiled at: 2020-01-27 12:43:28
# Size of source mod 2**32: 15004 bytes
import warnings, numpy as np
from scipy.linalg import eigh

def _trmag(xi, num, denom):
    """Helper used to find Lagrange multiplier for trust radius methods"""
    s = -num / (denom + xi)
    smag = np.linalg.norm(s)
    dsmag = -(s ** 2 / (denom + xi)).sum() / smag
    return (smag, dsmag)


def _root(fun, x0, target=0.0, args=tuple(), bounds=None, tol=1e-15, maxiter=100):
    """Finds x > 0 such that fun(x, *args) == target"""
    f, df = fun(x0, *args)
    err = f - target
    x = x0
    if bounds is None:
        bounds = [
         -np.infty, np.infty]
    else:
        bounds = list(bounds)
    if bounds[0] is None:
        bounds[0] = -np.infty
    if bounds[1] is None:
        bounds[1] = np.infty
    niter = 0
    while abs(err) > tol and niter < maxiter:
        x1 = x - err / df
        if x1 <= bounds[0]:
            x = (x + bounds[0]) / 2.0
        else:
            if x1 >= bounds[1]:
                x = (bounds[1] + x) / 2.0
            else:
                x = x1
        f, df = fun(x, *args)
        err = f - target
        niter += 1

    if abs(err) > tol:
        raise RuntimeError('Rootfinder failed!')
    return x


def rs_mmf(pes, g, r_tr, order=1, xi=1.0):
    """Perform a trust-radius Newton step towards an
    arbitrary-order saddle point (use order=0 to seek a minimum)"""
    if pes.lams is None:
        dx = -g
        dx_mag = np.linalg.norm(dx)
        bound_clip = False
        if dx_mag > r_tr:
            dx *= r_tr / dx_mag
            dx_mag = r_tr
            bound_clip = True
        return (dx, dx_mag, xi, bound_clip)
    else:
        L = np.abs(pes.lams)
        V = pes.vecs
        for i in range(order):
            g -= 2 * (V[:, i] @ g) * V[:, i]

        num = V.T @ g
        denom = L
        dx = -V @ (num / denom)
        dx_mag = np.linalg.norm(dx)
        if dx_mag <= r_tr:
            return (
             dx, dx_mag, xi, False)
        xi = _root(_trmag, xi, r_tr, args=(num, denom), bounds=[0.0, None])
        dx = -V @ (num / (denom + xi))
        dx_mag = np.linalg.norm(dx)
        assert abs(dx_mag - r_tr) < 1e-12
        return (dx, dx_mag, xi, True)


def rs_newton(pes, g, r_tr, order=1, xi=1.0):
    """Perform a trust-radius Newton step towards an
    arbitrary-order saddle point (use order=0 to seek a minimum)"""
    if pes.lams is None:
        dx = -g
        dx_mag = np.linalg.norm(dx)
        bound_clip = False
        if dx_mag > r_tr:
            dx *= r_tr / dx_mag
            dx_mag = r_tr
            bound_clip = True
        return (dx, dx_mag, xi, bound_clip)
    else:
        L = np.abs(pes.lams)
        L[:order] *= -1
        V = pes.vecs
        num = V.T @ g
        denom = L
        dx = -V @ (num / denom)
        dx_mag = np.linalg.norm(dx)
        if dx_mag <= r_tr:
            return (
             dx, dx_mag, xi, False)
        if order > 0:
            num *= L
            denom *= L
        xi = _root(_trmag, xi, r_tr, args=(num, denom), bounds=[0.0, None])
        dx = -V @ (num / (denom + xi))
        dx_mag = np.linalg.norm(dx)
        assert abs(dx_mag - r_tr) < 1e-12
        return (dx, dx_mag, xi, True)


def rs_rfo(pes, g, r_tr, order=0, alpha=0.5):
    Hmm = pes.H
    if Hmm is None:
        Hmm = np.eye(len(g))
    else:
        Hmm = pes.Tm.T @ pes.Tfree @ Hmm @ (pes.Tfree.T @ pes.Tm)
    H0 = np.block([[Hmm, g[:, np.newaxis]], [g, 0]])
    l, V = eigh(H0)
    s = V[:-1, order] / V[(-1, order)]
    smag = np.linalg.norm(s)
    if smag <= r_tr:
        return (s, smag, 1.0, False)
    else:
        lower = 0.0
        upper = 1.0
        alpha = r_tr / smag
        n = 1
        while abs(r_tr - smag) > 1e-15:
            if n >= 100:
                print(r_tr, smag, lower, alpha, upper)
                raise RuntimeError('RFO failed!')
            else:
                n += 1
                H = H0.copy() * alpha
                H[:-1, :-1] *= alpha
                l, V = eigh(H)
                s = V[:-1, order] * alpha / V[(-1, order)]
                smag = np.linalg.norm(s)
                if smag > r_tr:
                    upper = alpha
                else:
                    lower = alpha
            dHda = H0.copy()
            dHda[:-1, :-1] *= 2 * alpha
            dVda = V[:, :order] @ (V[:, :order].T @ dHda @ V[:, order] / (l[order] - l[:order])) + V[:, order + 1:] @ (V[:, order + 1:].T @ dHda @ V[:, order] / (l[order] - l[order + 1:]))
            dsda = V[:-1, order] / V[(-1, order)] + alpha / V[(-1, order)] * dVda[:-1] - V[:-1, order] * alpha / V[(-1, order)] ** 2 * dVda[(-1)]
            dsmagda = s @ dsda / smag
            err = smag - r_tr
            alpha -= err / dsmagda
            if np.isnan(alpha) or alpha <= lower or alpha >= upper:
                alpha = (lower + upper) / 2.0
            if np.nextafter(lower, upper) >= upper:
                break

        return (
         s, smag, alpha, True)


def rs_prfo(pes, g, r_tr, order=1, alpha=0.5):
    lams = pes.lams
    vecs = pes.vecs
    if lams is None:
        lams = np.ones_like(g)
        vecs = np.diag(lams)
    else:
        gmax = vecs[:, :order].T @ g
        gmin = vecs[:, order:].T @ g
        Hmax0 = np.block([[np.diag(lams[:order]), gmax[:, np.newaxis]],
         [
          gmax, 0]])
        Hmin0 = np.block([[np.diag(lams[order:]), gmin[:, np.newaxis]],
         [
          gmin, 0]])
        lmax, vmax = eigh(Hmax0)
        try:
            lmin, vmin = eigh(Hmin0)
        except np.linalg.LinAlgError:
            lmin, vmin = np.linalg.eigh(Hmin0)

        if vmax[(-1, -1)] == 0 or vmin[(-1, 0)] == 0:
            smag = np.infty
        else:
            smax = vmax[:-1, -1] / vmax[(-1, -1)]
        smin = vmin[:-1, 0] / vmin[(-1, 0)]
        s = vecs[:, :order] @ smax + vecs[:, order:] @ smin
        smag = np.linalg.norm(s)
    if smag <= r_tr:
        return (s, smag, 1.0, False)
    else:
        lower = 0.0
        upper = 1.0
        dHmax = np.zeros_like(Hmax0)
        dHmax[:, :-1] = 1.0
        dHmax[:-1, :] += 1.0
        dHmin = np.zeros_like(Hmin0)
        dHmin[:, :-1] = 1.0
        dHmin[:-1, :] += 1.0
        alpha = r_tr
        n = 1
        while abs(r_tr - smag) > 1e-15:
            if n >= 1000:
                raise RuntimeError('RFO failed!')
            else:
                n += 1
                Hmax = Hmax0.copy() * alpha
                Hmin = Hmin0.copy() * alpha
                Hmax[:-1, :-1] *= alpha
                Hmin[:-1, :-1] *= alpha
                lmax, vmax = eigh(Hmax)
                try:
                    lmin, vmin = eigh(Hmin)
                except np.linalg.LinAlgError:
                    lmin, vmin = np.linalg.eigh(Hmin)

                if vmax[(-1, -1)] == 0 or vmin[(-1, 0)] == 0:
                    smag = np.infty
                    upper = alpha
                    alpha = (lower + upper) / 2.0
                else:
                    smax = vmax[:-1, -1] * alpha / vmax[(-1, -1)]
                    smin = vmin[:-1, 0] * alpha / vmin[(-1, 0)]
                    s = vecs[:, :order] @ smax + vecs[:, order:] @ smin
                    smag = np.linalg.norm(s)
                    if smag > r_tr:
                        upper = alpha
                    else:
                        lower = alpha
            dHmaxda = Hmax0.copy()
            dHmaxda[:-1, :-1] *= 2 * alpha
            dHminda = Hmin0.copy()
            dHminda[:-1, :-1] *= 2 * alpha
            dvmaxda = vmax[:, :-1] @ (vmax[:, :-1].T @ dHmaxda @ vmax[:, -1] / (lmax[(-1)] - lmax[:-1]))
            dvminda = vmin[:, 1:] @ (vmin[:, 1:].T @ dHminda @ vmin[:, 0] / (lmin[0] - lmin[1:]))
            dsmaxda = vmax[:-1, -1] / vmax[(-1, -1)] + alpha / vmax[(-1, -1)] * dvmaxda[:-1] - vmax[:-1, -1] * alpha / vmax[(-1,
                                                                                                                             -1)] ** 2 * dvmaxda[(-1)]
            dsminda = vmin[:-1, 0] / vmin[(-1, 0)] + alpha / vmin[(-1, 0)] * dvminda[:-1] - vmin[:-1, 0] * alpha / vmin[(-1,
                                                                                                                         0)] ** 2 * dvminda[(-1)]
            dsmagda = (smin @ dsminda + smax @ dsmaxda) / smag
            err = smag - r_tr
            alpha -= err / dsmagda
            if np.isnan(alpha) or alpha <= lower or alpha >= upper:
                alpha = (lower + upper) / 2.0
            if np.nextafter(lower, upper) >= upper:
                break

        s = vecs[:, :order] @ smax + vecs[:, order:] @ smin
        return (s, smag, alpha, True)


def interpolate_quartic_constrained(f0, f1, g0, g1, dx, rmax=np.infty):
    """Constructs a 1-D quartic interpolation between two points given
    the function value and directional gradient at the endpoints, and
    finds and returns the extremum"""
    tmax = rmax / np.linalg.norm(dx)
    df = f1 - f0
    gdx0 = g0.T @ dx
    gdx1 = g1.T @ dx
    D = -6 * df ** 2 + 6 * df * (gdx0 + gdx1) - gdx0 ** 2 - 4 * gdx0 * gdx1 - gdx1 ** 2
    if D < 0:
        raise ValueError
    else:
        dg = g1 - g0
        sqrt2D = np.sqrt(2 * D)
        a_1 = 0.5 * (gdx1 - gdx0 - sqrt2D)
        a_2 = 0.5 * (gdx1 - gdx0 + sqrt2D)
        b_1 = -2 * a_1 - 2 * df + gdx0 + gdx1
        b_2 = -2 * a_2 - 2 * df + gdx0 + gdx1
        c_1 = a_1 + 3 * df - 2 * gdx0 - gdx1
        c_2 = a_2 + 3 * df - 2 * gdx0 - gdx1
        d = gdx0
        e = f0
        roots1 = np.roots([4 * a_1, 3 * b_1, 2 * c_1, d])
        for root in roots1:
            if root.imag == 0.0:
                t1 = min(root.real, tmax)
                break
        else:
            raise RuntimeError

        roots2 = np.roots([4 * a_2, 3 * b_2, 2 * c_2, d])
        for root in roots2:
            if abs(root.imag) < 1e-08:
                t2 = min(root.real, tmax)
                break
        else:
            raise RuntimeError

        ft1 = a_1 * t1 ** 4 + b_1 * t1 ** 3 + c_1 * t1 ** 2 + d * t1 + e
        ft2 = a_2 * t2 ** 4 + b_2 * t2 ** 3 + c_2 * t2 ** 2 + d * t2 + e
        if np.sign(gdx0 * (ft1 - f0)) == -1:
            t1 = -1.0
        if np.sign(gdx0 * (ft2 - f0)) == -1:
            t2 = -1.0
        if t1 < 0:
            if t2 < 0:
                raise ValueError
        if t1 < 0:
            t = t2
            ft = ft2
        else:
            if t2 < 0:
                t = t1
                ft = ft1
            else:
                if c_1 > 0:
                    df1 = min(f0, f1) - ft1
                else:
                    df1 = ft1 - max(f0, f1)
                if c_2 > 0:
                    df2 = min(f0, f1) - ft2
                else:
                    df2 = ft2 - max(f0, f1)
                if df2 > df1:
                    t = t2
                    ft = ft2
                else:
                    t = t1
                    ft = ft1
    gt = g0 + t * dg
    return (
     ft, gt, t)


def interpolate_cubic(f0, f1, g0, g1, dx, rmax=np.infty):
    tmax = rmax / np.linalg.norm(dx)
    df = f1 - f0
    gdx0 = g0.T @ dx
    gdx1 = g1.T @ dx
    dg = g1 - g0
    a = -2 * df + gdx0 + gdx1
    b = 3 * df - 2 * gdx0 - gdx1
    c = gdx0
    d = f0
    D = b ** 2 - 3 * a * c
    if D < 0:
        raise ValueError
    else:
        rad = np.sqrt(D)
        t1 = min((-b + rad) / (3 * a), tmax)
        t2 = min((-b - rad) / (3 * a), tmax)
        t = None
        if t1 < 0:
            raise ValueError
        else:
            if t2 < 0 or t1 < 1 and 1 - t1 > t2:
                t = t1
            else:
                t = t2
    ft = a * t ** 3 + b * t ** 2 + c * t + d
    gt = g0 + t * dg
    return (
     ft, gt, t)


def interpolate_quadratic(f0, f1, g0, g1, dx, rmax=np.infty):
    tmax = rmax / np.linalg.norm(dx)
    df = f1 - f0
    dg = g1 - g0
    gdx0 = g0.T @ dx
    gdx1 = g1.T @ dx
    if gdx1 / gdx0 > 1:
        t = tmax
    else:
        t = min(gdx0 / (gdx0 - gdx1), tmax)
    ft = f0 + t * df
    gt = g0 + t * dg
    return (
     ft, gt, t)


def optimize(mm, maxiter, gradtol, delta0=0.0013, sigma_inc=1.15, sigma_dec=0.65, rho_dec=5.0, rho_inc=1.035, order=1, eig=True, method='rsprfo', debug=False, **kwargs):
    if order != 0:
        if not eig:
            warnings.warn("Saddle point optimizations with eig=False will most likely fail!\n Proceeding anyway, but you shouldn't be optimistic.")
    else:
        if order > 1:
            warnings.warn('Optimization of saddle points with order greater than 1 has not been thoroughly tested.')
        delta = delta0 * len(mm.x_m)
        delta_min = kwargs.get('eta', delta / 100.0)
        f, g, _ = mm.kick(np.zeros_like(mm.x_m))
        if eig:
            (mm.f_pes)(**kwargs)
    alpha = 1.0
    niter = 0
    while 1:
        if method == 'gmtrm':
            s, smag, alpha, bound_clip = rs_newton(mm, g, delta, order, alpha)
        else:
            if method == 'mmf':
                s, smag, alpha, bound_clip = rs_mmf(mm, g, delta, order, alpha)
            else:
                if method == 'rsrfo' or method == 'rsprfo' and order == 0:
                    s, smag, alpha, bound_clip = rs_rfo(mm, g, delta, order, alpha)
                else:
                    if method == 'rsprfo':
                        if order > 0:
                            s, smag, alpha, bound_clip = rs_prfo(mm, g, delta, order, alpha)
                    ev = eig and mm.lams is not None and np.any(mm.lams[:order] > 0)
                    f, g, s = (mm.kick)(s, ev, **kwargs)
                    niter += 1
                    if mm.converged(gradtol) or mm.calls >= maxiter:
                        return (
                         mm.last['x'], niter)
                    rho = mm.ratio
                    if rho is None:
                        rho = 1.0
                if rho < 1.0 / rho_dec or rho > rho_dec:
                    delta = max(smag * sigma_dec, delta_min)
                elif 1.0 / rho_inc < rho < rho_inc:
                    delta = max(sigma_inc * smag, delta)
        if debug:
            print(f, np.linalg.norm(g), rho, smag / delta, delta, alpha, mm.lams[0])