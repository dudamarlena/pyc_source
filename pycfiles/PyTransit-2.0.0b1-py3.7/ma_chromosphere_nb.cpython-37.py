# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/pytransit/models/numba/ma_chromosphere_nb.py
# Compiled at: 2020-03-25 18:35:11
# Size of source mod 2**32: 8218 bytes
from numba import njit, prange
from numpy import pi, sqrt, abs, log, ones_like, zeros, atleast_2d, atleast_1d, nan
from orbits.orbits_py import z_ip_s
HALF_PI = 0.5 * pi
FOUR_PI = 4.0 * pi
INV_PI = 1 / pi

@njit(cache=False)
def ellpicb(n, k):
    """The complete elliptical integral of the third kind

    Bulirsch 1965, Numerische Mathematik, 7, 78
    Bulirsch 1965, Numerische Mathematik, 7, 353

    Adapted from L. Kreidbergs C version in BATMAN
    (Kreidberg, L. 2015, PASP 957, 127)
    (https://github.com/lkreidberg/batman)
    which is translated from J. Eastman's IDL routine
    in EXOFAST (Eastman et al. 2013, PASP 125, 83)"""
    kc = sqrt(1.0 - k * k)
    e = kc
    p = sqrt(n + 1.0)
    ip = 1.0 / p
    m0 = 1.0
    c = 1.0
    d = 1.0 / p
    for nit in range(1000):
        f = c
        c = d / p + c
        g = e / p
        d = 2.0 * (f * g + d)
        p = g + p
        g = m0
        m0 = kc + m0
        if abs(1.0 - kc / g) > 1e-08:
            kc = 2.0 * sqrt(e)
            e = kc * m0
        else:
            return HALF_PI * (c * m0 + d) / (m0 * (m0 + p))

    return 0.0


@njit(cache=False)
def ellec(k):
    a1 = 0.44325141463
    a2 = 0.0626060122
    a3 = 0.04757383546
    a4 = 0.01736506451
    b1 = 0.2499836831
    b2 = 0.09200180037
    b3 = 0.04069697526
    b4 = 0.00526449639
    m1 = 1.0 - k * k
    ee1 = 1.0 + m1 * (a1 + m1 * (a2 + m1 * (a3 + m1 * a4)))
    ee2 = m1 * (b1 + m1 * (b2 + m1 * (b3 + m1 * b4))) * log(1.0 / m1)
    return ee1 + ee2


@njit(cache=False)
def ellk(k):
    a0 = 1.38629436112
    a1 = 0.09666344259
    a2 = 0.03590092383
    a3 = 0.03742563713
    a4 = 0.01451196212
    b0 = 0.5
    b1 = 0.12498593597
    b2 = 0.06880248576
    b3 = 0.03328355346
    b4 = 0.00441787012
    m1 = 1.0 - k * k
    ek1 = a0 + m1 * (a1 + m1 * (a2 + m1 * (a3 + m1 * a4)))
    ek2 = (b0 + m1 * (b1 + m1 * (b2 + m1 * (b3 + m1 * b4)))) * log(m1)
    return ek1 - ek2


@njit(cache=False)
def chromosphere_z_v(zs, k):
    """Optically thin chromosphere model presented in
       Schlawin, Agol, Walkowicz, Covey & Lloyd (2010)"""
    nz = len(zs)
    flux = ones_like(zs)
    for i in range(nz):
        z = zs[i]
        if z > 0.0:
            if z - k < 1.0:
                zmk2 = (z - k) ** 2
                if z + k < 1.0:
                    t = sqrt(4.0 * z * k / (1.0 - zmk2))
                    flux[i] = 4.0 / sqrt(1.0 - zmk2) * ((zmk2 - 1.0) * ellec(t) - (z ** 2 - k ** 2) * ellk(t) + (z + k) / (z - k) * ellpicb(4.0 * z * k / zmk2, t))
                else:
                    if z + k > 1.0:
                        t = sqrt((1.0 - zmk2) / (4.0 * z * k))
                        flux[i] = 2.0 / (z - k) / sqrt(z * k) * (4.0 * z * k * (k - z) * ellec(t) + (-z + 2.0 * z ** 2 * k + k - 2.0 * k ** 3) * ellk(t) + (z + k) * ellpicb(1.0 / zmk2 - 1.0, t))
                if k > z:
                    flux[i] += FOUR_PI
            flux[i] = 1.0 - flux[i] / FOUR_PI

    return flux


@njit(cache=False)
def chromosphere_z_s(z, k):
    """Optically thin chromosphere model presented in
       Schlawin, Agol, Walkowicz, Covey & Lloyd (2010)"""
    if z < 0.0 or z > 1.0 + k:
        flux = 1.0
    else:
        zmk2 = (z - k) ** 2
        if z + k < 1.0:
            t = sqrt(4.0 * z * k / (1.0 - zmk2))
            flux = 4.0 / sqrt(1.0 - zmk2) * ((zmk2 - 1.0) * ellec(t) - (z ** 2 - k ** 2) * ellk(t) + (z + k) / (z - k) * ellpicb(4.0 * z * k / zmk2, t))
        else:
            if z + k > 1.0:
                t = sqrt((1.0 - zmk2) / (4.0 * z * k))
                flux = 2.0 / (z - k) / sqrt(z * k) * (4.0 * z * k * (k - z) * ellec(t) + (-z + 2.0 * z ** 2 * k + k - 2.0 * k ** 3) * ellk(t) + (z + k) * ellpicb(1.0 / zmk2 - 1.0, t))
            if k > z:
                flux += FOUR_PI
        flux = 1.0 - flux / FOUR_PI
    return flux


@njit(parallel=True, fastmath=True)
def chromosphere_model_v(t, k, t0, p, a, i, e, w, lcids, pbids, nsamples, exptimes, es, ms, tae):
    t0, p, a, i, e, w = (atleast_1d(t0), atleast_1d(p), atleast_1d(a), atleast_1d(i), atleast_1d(e), atleast_1d(w))
    k = atleast_2d(k)
    npv = k.shape[0]
    npt = t.size
    flux = zeros((npv, npt))
    for j in prange(npt):
        for ipv in range(npv):
            ilc = lcids[j]
            ipb = pbids[ilc]
            if k.shape[1] == 1:
                _k = k[(ipv, 0)]
            else:
                _k = k[(ipv, ipb)]
            for isample in range(1, nsamples[ilc] + 1):
                time_offset = exptimes[ilc] * ((isample - 0.5) / nsamples[ilc] - 0.5)
                z = z_ip_s(t[j] + time_offset, t0[ipv], p[ipv], a[ipv], i[ipv], e[ipv], w[ipv], es, ms, tae)
                if z > 1.0 + _k:
                    flux[(ipv, j)] += 1.0
                else:
                    flux[(ipv, j)] += chromosphere_z_s(z, _k)

            flux[(ipv, j)] /= nsamples[ilc]

    return flux


@njit(parallel=True, fastmath=True)
def chromosphere_model_s(t, k, t0, p, a, i, e, w, lcids, pbids, nsamples, exptimes, es, ms, tae):
    k = atleast_1d(k)
    npt = t.size
    flux = zeros(npt)
    for j in prange(npt):
        ilc = lcids[j]
        ipb = pbids[ilc]
        _k = k[0] if k.size == 1 else k[ipb]
        for isample in range(1, nsamples[ilc] + 1):
            time_offset = exptimes[ilc] * ((isample - 0.5) / nsamples[ilc] - 0.5)
            z = z_ip_s(t[j] + time_offset, t0, p, a, i, e, w, es, ms, tae)
            if z > 1.0 + _k:
                flux[j] += 1.0
            else:
                flux[j] += chromosphere_z_s(z, _k)

        flux[j] /= nsamples[ilc]

    return flux


@njit(parallel=True, fastmath=True)
def chromosphere_model_pv(t, pvp, lcids, pbids, nsamples, exptimes, es, ms, tae):
    pvp = atleast_2d(pvp)
    npv = pvp.shape[0]
    npt = t.size
    nk = pvp.shape[1] - 6
    flux = zeros((npv, npt))
    for j in prange(npt):
        for ipv in range(npv):
            t0, p, a, i, e, w = pvp[ipv, nk:]
            ilc = lcids[j]
            ipb = pbids[ilc]
            if nk == 1:
                k = pvp[(ipv, 0)]
            else:
                if ipb < nk:
                    k = pvp[(ipv, ipb)]
                else:
                    k = nan
            for isample in range(1, nsamples[ilc] + 1):
                time_offset = exptimes[ilc] * ((isample - 0.5) / nsamples[ilc] - 0.5)
                z = z_ip_s(t[j] + time_offset, t0, p, a, i, e, w, es, ms, tae)
                if z > 1.0 + k:
                    flux[(ipv, j)] += 1.0
                else:
                    flux[(ipv, j)] += chromosphere_z_s(z, k)

            flux[(ipv, j)] /= nsamples[ilc]

    return flux